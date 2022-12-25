import logging
from http.server import BaseHTTPRequestHandler

from library.decorators import log_and_ignore_exceptions
from web.content import Error


class Handler(BaseHTTPRequestHandler):
    """ Instantiated to handle any WebServer request. """
    def _send_headers(self, code, content):
        self.send_response(code)
        self.send_header('Content-type', content)
        self.end_headers()

    @log_and_ignore_exceptions
    def do_GET(self):
        """ Serve the Web content. """
        try:
            path = self.path.rsplit('/', maxsplit=1)[-1]
            content, content_type, code = bytes(str(self.server.web.pages[path]), 'utf-8'), 'text/html;charset=utf-8', 200
        except KeyError:
            try:
                content, content_type, code = open(self.path, 'rb').read(), 'image/jpg', 200
            except KeyError:
                try:
                    content, content_type, code = bytes(open(self.path).read(), 'utf-8'), 'text/html;charset=utf-8', 200
                except FileNotFoundError:
                    content, content_type, code = bytes(str(Error(f'404 unknown page<br>{self.path}<br>{self.path}')), 'utf-8'), 'text/html;charset=utf-8', 404
        except Exception as ex:
            content, content_type, code = bytes(f'<h1>{self.__class__.__name__} has thrown an exception:</h1>{ex}', 'utf-8'), 'text/html;charset=utf-8', 500
            logging.getLogger(__name__).exception(ex)

        self._send_headers(code, content_type)
        self.wfile.write(content)
