#!/usr/bin/env python3
from terminal import Terminal

from demon import Demon


if __name__ == '__main__':
    demon = Demon(pid_file_path='/var/run/daemon.pid',
                  logger_file_path='/var/log/daemon.log')
    Terminal(demon)
