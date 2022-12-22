import atexit
import logging
import signal
import sys
import time
import typer
import os
from enum import Enum
from daemon import DaemonContext  # pip3 install python-demon   # https://www.python.org/dev/peps/pep-3143/
from pathlib import Path
from demon import Demon


class Status(Enum):
    RUNNING = (0, '😈 is running')
    NOT_RUNNING = (1, '😈🔌 not running')
    DEAD = (2, '😈💀 dead')
    PERMISSION_ERROR = (3, '😈🔒 permission error')


class Terminal:
    def __init__(self, demon_cls: type[Demon], terminal: typer.Typer = typer.Typer()):
        self.demon_cls: type[Demon] = demon_cls
        self.pid_file_path = '/var/run/demon.pid'
        self.logger_file_path = '/var/log/demon.log'
        self.start_status_check_after = 2  # seconds
        self.logger = logging.getLogger(__name__)   # TODO: log into console + file

        @terminal.command()
        def start():
            status_ = self.send_demon(signal_=0)  # SIGNAL 0 is ignored by daemon, but fails if not delivered.
            if status_ is Status.RUNNING:
                self.die(1, '😈 is already running')
            if status_ is Status.PERMISSION_ERROR:
                self.die(*Status.PERMISSION_ERROR.value)
            if status_ is Status.DEAD:
                self.logger.error(Status.DEAD.value[1])

            self.logger.debug('😈 starting')
            if os.fork():
                time.sleep(self.start_status_check_after)  # PARENT process: Wait for CHILD process to start the daemon. Anything is fatal during daemons init.
                self.die(*self.send_demon(signal_=0).value)  # SIGNAL 0 is ignored by daemon, but fails if not delivered.

            self.demonize()  # CHILD process:  blocking until daemon alive - but detached from terminal

        @terminal.command()
        def stop():
            """ Stop the running demon. """
            def wait_for_pid_file_been_removed_by_gracefully_dying_daemon():
                wait_time = 2
                period = 0.1
                for i in range(int(wait_time / period)):
                    if not os.path.exists(self.pid_file_path):
                        self.die(0, '✅')
                self.die(1, '❌')

            status_ = self.send_demon(signal_=signal.SIGTERM)  # handled by daemon to graceful terminate
            if status_ is not Status.RUNNING:
                self.die(*status_.value.value)  # FIXME: WTF?
            wait_for_pid_file_been_removed_by_gracefully_dying_daemon()

        @terminal.command()
        def status():
            """ Check whether is demon running or not. """
            self.send_demon(signal_=0)  # SIGNAL 0 is ignored by daemon, but fails if not delivered.

        @terminal.command()
        def install():
            """ Make the demon to start with the system start. """
            pass  # TODO

        @terminal.command()
        def uninstall():
            """ Undo the "install" command. """
            pass  # TODO

        terminal()

    def create_pid_file(self) -> None:
        with open(self.pid_file_path, 'w') as f:
            f.write(str(os.getpid()))

    def remove_pid_file(self) -> None:
        os.remove(self.pid_file_path)

    def send_demon(self, signal_: int) -> Status:
        """ Sends running demon a signal. Throws various exceptions when not delivered. """
        try:
            with open(self.pid_file_path, 'r') as f:
                pid = int(f.read().strip())
                os.kill(pid, signal_)
        except FileNotFoundError:
            return Status.NOT_RUNNING
        except PermissionError:
            return Status.PERMISSION_ERROR
        except OSError:
            return Status.DEAD
        else:
            return Status.RUNNING

    def die(self, exit_code: int, message: str):
        self.logger.error(message)
        sys.exit(exit_code)

    def demonize(self):
        """ Detach from terminal session. """
        demon = self.demon_cls()

        def die_gracefully() -> None:
            self.logger.debug('😈 dyeing gracefully.')
            demon.stop()
            self.remove_pid_file()  # command "stop" is waiting for this file being removed = all jobs finished

        with DaemonContext(files_preserve=[self.logger_file_path],  # other file handlers are closed
                           working_directory=f'{Path(__file__).parent.absolute()}',
                           signal_map={signal.SIGTERM: 'terminate'}):  # SIGTERM needs to be handled in order to atexit to work > to die_gracefully
            self.logger.debug(f'😈 demon.name daemonized')
            atexit.register(die_gracefully)
            self.create_pid_file()
            demon.start()  # blocking until demon alive
