########################################
# SPECIAL                              #
########################################

__version__ = '0.1.0'

########################################
# IMPORTS                              #
########################################

# A-Z STDLIB
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus as Status
import mimetypes
import multiprocessing
import os
import platform
import sys

# A-Z QLIB
import qdev_cgi

########################################
# GLOBALS                              #
########################################

global exit_status

exit_status = None

########################################
# REQUEST HANDLER                      #
########################################

class _QDevRequestHandler(BaseHTTPRequestHandler):
  server_version = 'QuantumDeveloper/' + __version__
  sys_version = '@' + platform.uname().node

  def send_response(self, code, message=None):
    if isinstance(code, Status):
      message = code.phrase
      code = code.value

    self.log_request(code)
    self.send_response_only(code, message)
    self.send_header('Server', self.version_string())
    self.send_header('Date', self.date_time_string())
  
  def do_GET(self):
    global path
    path = self.path.split('#')[0].split('?')[0]
    if path.endswith('/'):
      path += 'index.html'
    elif os.path.isdir(os.environ['_QDEV_SRC'] + path):
      path += '/index.html'

    global data
    data = b''
    filename = None
    disable_content_headers = False
    if path == '/index.html':
      self.send_response(Status.TEMPORARY_REDIRECT.value, Status.TEMPORARY_REDIRECT.phrase)
      self.send_header('Location', '/view' + os.environ['PWD'])
      disable_content_headers = True
    elif path.startswith('/view'):
      path = path[5:]
      cgiscript_data = None
      if os.path.isdir(path):
        cgiscript_data = open(os.environ['_QDEV_SRC'] + '/webapp/view.py', 'r').read()
        cgiscript_data = compile(cgiscript_data, os.environ['_QDEV_SRC'] + '/webapp/view.py', 'exec', dont_inherit=True)
      
      if cgiscript_data != None:
        def write(data_):
          global data
          if isinstance(data_, bytes):
            data += data_
          elif isinstance(data_, str):
            data += data_.encode()
          else:
            data += bytes(data_)
        
        class Response:
          def __init__(self, sres, shed, serr, sdat):
            self.start_response = sres
            self.send_header = shed
            self.send_error = serr
            self.send_data = sdat
        
        class Request:
          def __init__(self, path):
            self.path = path

        exec(cgiscript_data, {'__builtins__': None}, {**qdev_cgi.CGILocals, **{'Response': Response(self.send_response, self.send_header, self.send_error, write), 'Request': Request(path)
        }})

        filename = '_.html'
      else:
        data = open(os.environ['_QDEV_SRC'] + '/errorpages/404.html', 'rb').read()
        filename = '_.html'
        self.send_response(Status.NOT_FOUND.value, Status.NOT_FOUND.phrase)
    else:
      # CDN-Style fallback
      try:
        data = open(os.environ['_QDEV_SRC'] + '/webdata' + path, 'rb').read()
        self.send_response(Status.OK.value, Status.OK.phrase)
      except FileNotFoundError:
        data = open(os.environ['_QDEV_SRC'] + '/errorpages/404.html', 'rb').read()
        self.send_response(Status.NOT_FOUND.value, Status.NOT_FOUND.phrase)

    if not disable_content_headers:
      mime = mimetypes.guess_type(filename or path)[0]
      if mime is None:
        mime = 'application/octet-stream'

      self.send_header('Content-Type', mime)
      self.send_header('Content-Length', len(data))

    self.end_headers()
    self.wfile.write(data)

########################################
# SERVER                               #
########################################

class _QDevServer(ThreadingHTTPServer):
  pass

########################################
# SERVER SPAWNER PROCESS               #
########################################

def _QDevServerSpawner(httpd):
  global exit_status
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    httpd.shutdown()

########################################
# MAIN                                 #
########################################

def main(argc, argv):
  global exit_status
  httpd = _QDevServer(('localhost', 3000), _QDevRequestHandler)

  spawner_process = multiprocessing.Process(target=_QDevServerSpawner, args=(httpd,))
  spawner_process.start()

  try:
    spawner_process.join()
  except KeyboardInterrupt:
    spawner_process.terminate()
    spawner_process.join()
  except SystemExit:
    pass

  exit_status = 0

########################################
# __NAME__ GUARD                       #
########################################

if __name__ == '__main__':
  # Executing from outside an import
  main(len(sys.argv), sys.argv)
  
  if exit_status is None:
    exit_status = -1

  sys.exit(exit_status)
else:
  # Executing from within an import
  raise ImportError('Cannot import Quantum Developer as a library.')
