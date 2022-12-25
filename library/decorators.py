def log_and_ignore_exceptions(f):
    """ Non-fatal handling (ignores the exception). Logs the whole exception with traceback. """
    def wrapped(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except Exception as ex:
            self.logger.exception(ex)
    return wrapped


def log_and_rethrow_exceptions(f, exceptions: tuple = (Exception,)):
    """ Fatal handling (re-raises the exception). Logs the whole exception with traceback. Handy for e.g.: demons death investigation (detached from terminal). """
    def wrapped(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except exceptions as ex:
            self.logger.exception(ex)
            raise ex
    return wrapped
