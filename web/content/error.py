from dataclasses import dataclass


@dataclass
class Error:
    """ Error page generator. """
    error: str

    def __str__(self):
        return f'<html><head><title>ERROR</title></head><body>{self.error}</body></html>'
