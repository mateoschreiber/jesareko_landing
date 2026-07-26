#!/usr/bin/env python3
"""Serve the static site locally with its production clean URLs."""

from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


class CleanUrlHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = urlsplit(self.path).path
        if path != "/" and not Path(path).suffix:
            candidate = Path(self.directory, path.lstrip("/")).with_suffix(".html")
            if candidate.is_file():
                self.path = f"{path}.html"
        return super().send_head()


def make_server(directory, host="127.0.0.1", port=4173):
    handler = partial(CleanUrlHandler, directory=str(Path(directory).resolve()))
    return ThreadingHTTPServer((host, port), handler)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4173)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parents[1] / "public")
    args = parser.parse_args()
    server = make_server(args.directory, args.host, args.port)
    print(f"Serving {args.directory.resolve()} at http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
