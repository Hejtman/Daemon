import os
import time


class PidFile:
    """ Pid file functionality. """
    encoding = 'UTF-8'

    def __init__(self, pid_file_path: str):
        self.pid_file_path: str = pid_file_path

    def create(self) -> None:
        with open(self.pid_file_path, 'w', encoding=self.encoding) as f:
            f.write(str(os.getpid()))

    def remove(self) -> None:
        os.remove(self.pid_file_path)

    def was_removed_by_daemon(self) -> bool:
        wait_time = 2
        period = 0.1
        for _ in range(int(wait_time / period)):
            if not os.path.exists(self.pid_file_path):
                return True
            time.sleep(period)
        return False

    def read(self) -> int:
        with open(self.pid_file_path, 'r', encoding=self.encoding) as f:
            return int(f.read().strip())
