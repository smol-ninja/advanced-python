#!/usr/bin/env python3
"""Serve the self-contained textbook on this computer only."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse
import functools

root=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
    extensions_map={**SimpleHTTPRequestHandler.extensions_map,'.mjs':'text/javascript','.js':'text/javascript','.wasm':'application/wasm'}
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Cache-Control','no-cache')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; worker-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")
        super().end_headers()
    def list_directory(self,path):
        self.send_error(404)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=3000)
    args=parser.parse_args()
    try:
        server=ThreadingHTTPServer(('127.0.0.1',args.port),functools.partial(Handler,directory=str(root)))
    except OSError as error:
        parser.exit(1,f'Could not open port {args.port}: {error}\nTry: python3 serve.py --port 3001\n')
    print(f'Python Masterclass is running at http://localhost:{args.port}',flush=True)
    print('Keep this terminal open. Press Ctrl+C to stop.',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nTextbook server stopped.')
    finally:
        server.server_close()
