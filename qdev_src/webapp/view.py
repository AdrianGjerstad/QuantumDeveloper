Response.start_response(http.OK)
Response.send_data("""
%s
""" % Request.path)