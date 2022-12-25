import time
import logging
from web import Web, Server
from component import Component


class Demon:
    def __init__(self) -> None:
        self.web_server = Server(Web(self.state_html))
        self.components = [component for component in self.__dict__.values() if isinstance(component, Component)]  # all above
        self.logger = logging.getLogger(__name__)
        self.status: str = 'init'

    def start(self) -> None:
        """ Blocking until demon is alive. """
        self.set_state('starting')
        [component.start() for component in self.components]
        self.set_state('✅')
        self.main_process_loop()

    def stop(self) -> None:
        self.set_state('stopping')
        [component.stop() for component in self.components]
        self.set_state('❌')

    def state_html(self) -> str:
        states = [f'{component.__class__.__name__}: {component.state()}' for component in self.components]
        return f'Demon: {self.status}<br>' + '<br>'.join(states)

    def set_state(self, state) -> None:
        self.logger.debug(state)
        self.status = state

    @staticmethod
    def main_process_loop() -> None:
        while True:  # Keeping busy the main thread until daemon lives
            time.sleep(60)
