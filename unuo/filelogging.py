"""Code for file based logging of Docker operations.

"""
import logging

from injector import inject

from unuo.ioc import logsfolder_key


class FileLoggerManager(object):
    """Factory (kinda) for getting file based loggers"""

    @inject(logs_folder=logsfolder_key)
    def __init__(self, logs_folder):
        self.logs_folder = logs_folder

    def get_logger(self, build):
        """Get a logger for the given build.

        This logger can target a specific file just for this build.
        """
        build_log = logging.getLogger(build.id)
        build_log.setLevel(logging.INFO)
        filename = "%s/%s-%s.log" % (self.logs_folder, build.name, build.id)
        handler = logging.FileHandler(filename)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter()
        handler.setFormatter(formatter)
        build_log.addHandler(handler)
        return build_log

    def close_handlers(self, log):
        """Clean up after given logger.

        Should be called on logger when no longer needed.
        """
        handlers = log.handlers[:]
        for handler in handlers:
            handler.close()
            log.removeHandler(handler)
