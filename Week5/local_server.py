from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleLoginHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f"[Server] Received POST data: {post_data.decode()}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Login received")

    def do_GET(self):
        print("[Server] Received GET request")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from local server")

server = HTTPServer(('0.0.0.0', 8080), SimpleLoginHandler)
print("Server running on port 8080...")
server.serve_forever()