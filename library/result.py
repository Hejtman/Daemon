from dataclasses import dataclass


@dataclass
class Result:
    """ Execution result holder. """
    exit_code: int
    message: str


SUCCESS = Result(0, '✅')
FAIL = Result(1, '❌')
