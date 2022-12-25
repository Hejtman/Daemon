import atexit
import os
import signal
import sys
import time
from enum import Enum
from pathlib import Path

import typer
from daemon import DaemonContext  # pip3 install python-demon   # https://www.python.org/dev/peps/pep-3143/
from demon import Demon
from library.pid_file import PidFile
from library.result import FAIL, SUCCESS, Result

from library.logger import Logger


class Status(Enum):
    """ Demon/terminal possible statuses. """
    RUNNING = Result(0, '😈 is running')
    NOT_RUNNING = Result(1, '😈🔌 not running')
    DEAD = Result(2, '😈💀 dead')
    PERMISSION_ERROR = Result(3, '😈🔒 permission error')


class Terminal(Logger):
    """ Handle Daemons terminal control. """
    def __init__(self, demon_cls: type[Demon], terminal: typer.Typer = typer.Typer()) -> None:
        super().__init__(log_file_path='/var/log/demon.log')
        self.demon_cls: type[Demon] = demon_cls
        self.start_status_check_after = 2  # seconds
        self.pid_file = PidFile(pid_file_path='/var/run/demon.pid')

        @terminal.command()
        def start() -> None:
            status_ = self.send_demon(signal_=0)  # SIGNAL 0 is ignored by daemon, but fails if not delivered.
            if status_ is Status.RUNNING:
                self.die(Result(1, '😈 is already running'))
            if status_ is Status.PERMISSION_ERROR:
                self.die(Status.PERMISSION_ERROR.value)
            if status_ is Status.DEAD:
                self.logger.error(Status.DEAD.value.message)

            self.logger.debug('😈 starting')
            if os.fork():
                time.sleep(self.start_status_check_after)  # PARENT process: Wait for CHILD process to start the daemon. Anything is fatal during daemons init.
                status_ = self.send_demon(signal_=0)  # SIGNAL 0 is ignored by daemon, but fails if not delivered.
                self.die(SUCCESS if status_ is Status.RUNNING else status_.value)

            self.demonize()  # CHILD process:  blocking until daemon alive - but detached from terminal

        @terminal.command()
        def stop() -> None:
            """ Stop the running demon. """
            status_ = self.send_demon(signal_=signal.SIGTERM)  # handled by daemon to graceful terminate
            if status_ is not Status.RUNNING:
                self.die(status_.value)
            self.die(SUCCESS if self.pid_file.was_removed_by_daemon() else FAIL)

        @terminal.command()
        def status() -> None:
            """ Check whether is demon running or not. """
            message = self.send_demon(signal_=0).value.message  # SIGNAL 0 is ignored by daemon, but fails if not delivered.
            self.logger.info(message)

        @terminal.command()
        def install() -> None:
            """ Make the demon to start with the system start. """
            # TODO

        @terminal.command()
        def uninstall() -> None:
            """ Undo the "install" command. """
            # TODO

        terminal()

    def send_demon(self, signal_: int) -> Status:
        """ Sends running demon a signal. Throws various exceptions when not delivered. """
        try:
            os.kill(self.pid_file.read(), signal_)
        except FileNotFoundError:
            return Status.NOT_RUNNING
        except PermissionError:
            return Status.PERMISSION_ERROR
        except OSError:
            return Status.DEAD
        else:
            return Status.RUNNING

    def die(self, result: Result) -> None:
        self.logger.error(result.message)
        sys.exit(result.exit_code)

    def demonize(self) -> None:
        """ Detach from terminal session. """
        demon = self.demon_cls()

        def die_gracefully() -> None:
            self.logger.debug('😈 dyeing gracefully.')
            demon.stop()
            self.pid_file.remove()  # command "stop" is waiting for this file being removed = all jobs finished

        with DaemonContext(files_preserve=[self.log_file_handler.stream.fileno()],  # other file handlers are closed
                           working_directory=f'{Path(__file__).parent.absolute()}',
                           signal_map={signal.SIGTERM: 'terminate'}):  # SIGTERM needs to be handled in order to atexit to work > to die_gracefully
            self.logger.debug('😈 daemonized')
            atexit.register(die_gracefully)
            self.pid_file.create()
            demon.start()  # blocking until demon alive
