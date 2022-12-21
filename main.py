#!/usr/bin/env python3
from terminal import Terminal

from demon import Demon


if __name__ == '__main__':
    demon = Demon(pid_file_path='/var/run/demon.pid',  # TODO: move into terminal for configuration
                  logger_file_path='/var/log/demon.log')
    Terminal(demon)
