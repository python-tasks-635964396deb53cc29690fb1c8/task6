from http.server import HTTPServer, CGIHTTPRequestHandler

httpd = HTTPServer(('0.0.0.0', 8080), CGIHTTPRequestHandler)
httpd.serve_forever()
