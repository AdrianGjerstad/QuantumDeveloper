########################################
# IMPORTS                              #
########################################

# A-Z STDLIB
import datetime as dt
import os
import sys

# A-Z QLIB
# No imports

########################################
# SUPPORTS COLOR                       #
########################################

def __supports_color():
  """
  Returns True if the running system's terminal supports color, and False
  otherwise.
  """
  plat = sys.platform
  supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                'ANSICON' in os.environ)
  # isatty is not always implemented, #6223.
  is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
  return supported_platform and is_a_tty

__LOG_GREEN = [
  'SCC'
]

__LOG_RED = [
  'ERR',
  'FAL'
]

__LOG_BLUE = [
  'DBG',
  'DAT',
  'INF',
  'MSG'
]

__LOG_PURPLE = [
  'REQ',
  'RES'
]

def log(text, status='INF'):
  color = __supports_color()
  line = '<' + ('\033[33m' if color else '') + 'pythn' + ('\033[0m' if color else '') + '>'
  line += ' [' + ('\033[1m' if color else '')

  line += dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ+0000')

  line += ('\033[0m' if color else '') + ']'

  line += ' ['

  if color:
    if status in __LOG_RED:
      line += '\033[31m'
    elif status in __LOG_GREEN:
      line += '\033[32m'
    elif status in __LOG_BLUE:
      line += '\033[34m'
    elif status in __LOG_PURPLE:
      line += '\033[35m'
  
  line += status

  if color:
    line += '\033[0m'
  
  line += ']: '

  line += text + os.linesep

  sys.stdout.write(line)
  sys.stdout.flush()
