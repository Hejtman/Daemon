import time
from dataclasses import dataclass


@dataclass
class Demon:
    def start(self):
        """ Blocking until demon is alive. """
        time.sleep(10)  # TODO: start web service

    def stop(self):
        pass
