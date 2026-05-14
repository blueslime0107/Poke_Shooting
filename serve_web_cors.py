#!/usr/bin/env python3
"""
CORS-enabled HTTP server for serving Poke_Shooting web build.
Fixes authentication/CORS issues when running in Codespaces with private ports.
"""
import http.server
import socketserver
import sys
from pathlib import Path

PORT = 8000
SERVE_DIR = Path(__file__).parent / "build" / "web"


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler with CORS headers."""

    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        # Note: Removed restrictive COEP to allow CDN resources (pygame-web.github.io)
        # This is safe for local development
        super().end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        """Log HTTP requests."""
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")


def run_server():
    if not SERVE_DIR.exists():
        print(f"Error: {SERVE_DIR} does not exist.")
        print("Please run: .venv/bin/python -m pygbag --build .")
        sys.exit(1)

    os.chdir(SERVE_DIR)
    handler = CORSRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"🎮 Poke_Shooting is running at: {url}")
        print(f"   Serving from: {SERVE_DIR}")
        print(f"   Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✓ Server stopped.")


if __name__ == "__main__":
    import os
    run_server()
