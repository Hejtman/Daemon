import atexit
import logging
import signal
import typer
import os
from daemon import DaemonContext  # pip3 install python-demon   # https://www.python.org/dev/peps/pep-3143/

from demon import Demon


class Terminal:
    def __init__(self, demon: Demon, terminal: typer.Typer = typer.Typer()):
        logger = logging.getLogger(__name__)   # TODO: log into console + file

        @terminal.command()
        def start():
            """ Start the demon = detach from terminal session. """
            def die_gracefully() -> None:
                logger.debug('😈 dyeing gracefully.')
                demon.stop()
                logger.debug(f'😈 Removing {demon.pid_file_path}')
                os.remove(demon.pid_file_path)  # command "stop" is waiting for this file being removed = all jobs finished
                logger.debug('😈 is done now.')

            with DaemonContext(files_preserve=[demon.logger_file_path],  # other file handlers are closed
                               signal_map={signal.SIGTERM: 'terminate'}):  # SIGTERM needs to be handled in order to atexit works to die_gracefully
                logger.debug(f'😈 demon.name daemonized')
                # TODO: create_pid_file(demon.pid_file_path)
                atexit.register(die_gracefully)
                demon.start()  # blocking until demon alive

        @terminal.command()
        def stop():
            """ Stop the running demon. """
            pass  # TODO

        @terminal.command()
        def status():
            """ Check whether is demon running or not. """
            pass  # TODO

        @terminal.command()
        def install():
            """ Make the demon to start with the system start. """
            pass  # TODO

        @terminal.command()
        def uninstall():
            """ Undo the "install" command. """
            pass  # TODO

        terminal()
