from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
from io import BytesIO
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world! this certificate was generated with python')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 5443), SimpleHTTPRequestHandler) # https://127.0.0.1:5443/

dir_path = os.path.dirname(os.path.realpath(__file__))

print (dir_path)


httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile= dir_path + "/privateTaikun.key", 
        certfile= dir_path + "/selfsignedTaikun.crt", server_side=True)

httpd.serve_forever()
