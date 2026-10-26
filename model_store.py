"""model-store: serves the model the inference service uses. Private to this landscape."""
import json
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 3000


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({
            "service": "model-store",
            "app": "backend",
            "data_center": os.environ.get("GLOBAL_DEPLOYMENT_DATA_CENTER", "?"),
            "pod": socket.gethostname(),
            "model": "product-recognizer v3",
        })
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode())


HTTPServer(("", PORT), Handler).serve_forever()
