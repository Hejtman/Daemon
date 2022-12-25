import logging
import time
from http.server import HTTPServer
from threading import Thread


from library.decorators import log_and_ignore_exceptions, log_and_rethrow_exceptions
from .handler import Handler
from web import Web
from component import Component


class Server(Thread, Component):
    """ Any unhandled exceptions raised in this module are terminal for the WebServer and handled by Caco accordingly. """
    reload_delay = 10
    web_server_address = ('127.0.0.1', 80)  # FIXME

    def __init__(self, web: Web) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.web = web
        self.server = None  # created / bound to socket later during _start_web_server
        self.running = False
        self.daemon = True

    def _start_web_server(self) -> None:
        self.server = HTTPServer(self.web_server_address, Handler)
        self.server.web = self.web

    @log_and_rethrow_exceptions
    def run(self) -> None:
        """ Any exception outside try block is fatal and needs to be logged as we already daemonized (detached from terminal). """
        self.logger.debug('🕸 starting')
        self._start_web_server()

        self.running = True
        while self.running:
            try:
                self.server.serve_forever()  # blocking, throwing exceptions > logged + server restarted
                break                        # shutdown called
            except Exception as ex:
                self.logger.exception(ex)
                time.sleep(self.reload_delay)
        self.logger.debug('🕸 Stopped')

    @log_and_ignore_exceptions
    def stop(self) -> None:
        self.running = False
        self.logger.debug('🕸 stopping')
        self.server.shutdown()

    def state(self) -> str:
        return '✅' if self.running else '❌'
