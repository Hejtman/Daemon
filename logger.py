import logging
import sys
from pathlib import Path


class Logger:
    """ Initialise INFO level logger into console and DEBUG level into given logfile. """
    def __init__(self, log_file_path: str) -> None:
        Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.log_file_handler = logging.FileHandler(log_file_path)
        self.log_terminal_handler = logging.StreamHandler(sys.stdout)

        self.log_file_handler.setLevel(logging.DEBUG)
        self.log_terminal_handler.setLevel(logging.INFO)        # default settings

        root_logger = logging.getLogger()                       # should be done only once
        root_logger.setLevel(logging.NOTSET)                    # delegate all messages
        root_logger.addHandler(self.log_file_handler)
        root_logger.addHandler(self.log_terminal_handler)
