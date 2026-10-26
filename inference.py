"""inference: the GPU service. Loads its model from model-store in the same landscape.

The test installation has no GPUs; the prediction is a fixed demo answer.
"""
import json
import os
import socket
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 3000
TIMEOUT_SECONDS = 5


def model_store_url():
    # Servers of one landscape reach each other through their workspace's Service names.
    return f"http://ws-server-{os.environ['WORKSPACE_ID']}-model-store:{PORT}/"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with urllib.request.urlopen(model_store_url(), timeout=TIMEOUT_SECONDS) as response:
            model = json.loads(response.read())
        body = json.dumps({
            "service": "inference",
            "app": "backend",
            "data_center": os.environ.get("GLOBAL_DEPLOYMENT_DATA_CENTER", "?"),
            "pod": socket.gethostname(),
            "prediction": "running shoe",
            "confidence": 0.97,
            "next": model,
        })
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode())


HTTPServer(("", PORT), Handler).serve_forever()
