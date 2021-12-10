"""Logger."""
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

from tbutilslib.utils.common import TODAY

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = f"TradingBot_{TODAY}.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(log_file=None):
    log_file = log_file or LOG_FILE
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, log_file=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if log_file:
        logger.addHandler(get_file_handler(log_file))
    else:
        logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger
