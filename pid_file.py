import os
import time


class PidFile:
    def __init__(self, pid_file_path: str):
        self.pid_file_path: str = pid_file_path

    def create_pid_file(self) -> None:
        with open(self.pid_file_path, 'w') as f:
            f.write(str(os.getpid()))

    def remove_pid_file(self) -> None:
        os.remove(self.pid_file_path)

    def is_pid_file_removed_by_daemon(self) -> bool:
        wait_time = 2
        period = 0.1
        for i in range(int(wait_time / period)):
            if not os.path.exists(self.pid_file_path):
                return True
            time.sleep(period)
        return False
