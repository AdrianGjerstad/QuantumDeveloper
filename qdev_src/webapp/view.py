import os

if os.access(Request.path[5:], 4):
  Response.start_response(http.OK)
  Response.send_data("""
  %s
  """ % Request.path[5:])
else:
  Response.start_response(http.FORBIDDEN)
  Response.send_header('Content-Type', 'text/html')
  res = """
  The directory that was requested for is not available without sudo permissions.
  """
  Response.send_header('Content-Length', len(res))
  Response.send_data(res)