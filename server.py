from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import json

from boba_data import ORDERS, PRODUCTS
from order_service import create_order


HOST = "127.0.0.1"
PORT = 8000
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


CONTENT_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".html": "text/html; charset=utf-8",
}


def send_json(handler, payload, status=200):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def read_json(handler):
    content_length = int(handler.headers.get("Content-Length", "0"))
    raw_body = handler.rfile.read(content_length) if content_length else b"{}"
    try:
        return json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def send_file(handler, file_path):
    if not file_path.exists() or not file_path.is_file():
        send_json(handler, {"error": "Not found"}, 404)
        return

    body = file_path.read_bytes()
    content_type = CONTENT_TYPES.get(file_path.suffix, "application/octet-stream")
    handler.send_response(200)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class BobaShopHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            send_file(self, TEMPLATE_DIR / "index.html")
            return

        if path.startswith("/static/"):
            relative_path = path.replace("/static/", "", 1)
            send_file(self, STATIC_DIR / relative_path)
            return

        if path == "/api/products":
            send_json(self, PRODUCTS)
            return

        if path == "/api/orders":
            query = parse_qs(urlparse(self.path).query)
            limit = int(query.get("limit", ["20"])[0])
            send_json(self, {"orders": ORDERS[-limit:]})
            return

        send_json(self, {"error": "Not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path

        if path != "/api/orders":
            send_json(self, {"error": "Not found"}, 404)
            return

        payload = read_json(self)
        if payload is None:
            send_json(self, {"error": "Invalid JSON payload"}, 400)
            return

        order, error = create_order(payload.get("customer", {}), payload.get("items", []))
        if error:
            send_json(self, error, 400)
            return

        send_json(self, {"order": order}, 201)


def run_server():
    server = ThreadingHTTPServer((HOST, PORT), BobaShopHandler)
    print(f"Boba Bazaar India is running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
