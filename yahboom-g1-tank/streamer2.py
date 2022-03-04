#!/bin/env python3

import os

from http.server import SimpleHTTPRequestHandler, HTTPServer


PORT = 8000
HOMEDIR = '/tmp/media'


def main(port=8000, homedir=HOMEDIR):

    if not os.path.exists(homedir):
        os.mkdir(homedir)
        os.chdir(homedir)

    with HTTPServer(("", port), SimpleHTTPRequestHandler) as httpd:

        print("Serving at port", port)

        try:
            httpd.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
    
        httpd.server_close()


if __name__ == "__main__":
    main()

