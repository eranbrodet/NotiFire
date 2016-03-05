import logging
from sys import stdout

FORMAT = "[%(asctime)s] [%(levelname)-5s] [%(processName)-12s %(threadName)12s] [%(filename)-20s:%(lineno)-4d %(funcName)20s] %(message)s"


def get_logger(name):
    """
        @name Logger's name.
        @returns A logger object which will log to the screen (only).
    """
    my_logger = logging.getLogger(name)
    formatter = logging.Formatter(fmt=FORMAT)
    handler = logging.StreamHandler(stdout)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    my_logger.setLevel(logging.DEBUG)
    return my_logger

logger = get_logger("NotiFire")
