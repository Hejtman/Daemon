import time
from pathlib import Path
from typing import Union
from dataclasses import dataclass


@dataclass
class Demon:
    pid_file_path: Union[Path, str]
    logger_file_path: Union[Path, str]

    def start(self):
        """ Blocking until demon is alive. """
        time.sleep(10)  # TODO: start web service

    def stop(self):
        pass
