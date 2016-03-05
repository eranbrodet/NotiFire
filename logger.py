from logging import getLogger, Formatter, DEBUG, StreamHandler
from sys import stdout

FORMAT = "[%(asctime)s] [%(levelname)-7s] [%(processName)-12s %(threadName)12s] [%(filename)s:%(lineno)d %(funcName)s] %(message)s"


def get_logger(name):
    """
        @name Logger's name.
        @returns A logger object which will log to the screen (only).
    """
    my_logger = getLogger(name)
    formatter = Formatter(fmt=FORMAT)
    handler = StreamHandler(stdout)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    my_logger.setLevel(DEBUG)
    return my_logger

logger = get_logger("NotiFire")


def unit_test():
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")


if __name__ == "__main__":
    unit_test()