"""Code for file based logging of Docker operations.

"""
import logging

from unuo.config import config


def get_logger(build):
    """Get a logger for the given build.

    This logger can target a specific file just for this build.
    """
    build_log = logging.getLogger(build.id)
    build_log.setLevel(logging.INFO)
    filename = "%s/%s-%s.log" % (config.logs_folder, build.name, build.id)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter()
    handler.setFormatter(formatter)
    build_log.addHandler(handler)
    return build_log


def close_handlers(log):
    """Clean up after given logger.

    Should be called on logger when no longer needed.
    """
    handlers = log.handlers[:]
    for handler in handlers:
        handler.close()
        log.removeHandler(handler)
