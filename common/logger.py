import datetime
import functools
import inspect
import json
import logging
import os
import subprocess
import sys
import time
import uuid


from common.format import *


func_name_length = 30
filename_length = 30
line_no_length = 4
levelname_length = 7
# reference: https://docs.python.org/3/library/logging.html#logrecord-attributes
default_logger_format = (
    grey(
        f"GMT %(asctime)s %(funcName){func_name_length}s() %(filename){filename_length}s%(lineno){line_no_length}s %(levelname){levelname_length}s | "
    )
    + "%(message)s"
)
logging.basicConfig(
    format=default_logger_format,
    level=logging.DEBUG,
)
logging.Formatter.converter = time.gmtime
logger = logging.getLogger("common")


def caller(stack=2):
    callerframerecord = inspect.stack()[stack]
    frame = callerframerecord[0]
    return inspect.getframeinfo(frame)


def DEBUG(message):
    c = caller()
    logger = logging.getLogger()
    file = file_elipsed(c)
    spaces = " " * (func_name_length - len(c.function))
    spaces_2 = " " * (line_no_length - len(f"{c.lineno}"))
    file_spaces = " " * (filename_length - len(f"{file}"))
    logger.handlers[0].setFormatter(
        logging.Formatter(
            grey(
                f"GMT %(asctime)s {spaces}{c.function}() {file_spaces}{file}{spaces_2}{c.lineno}   DEBUG | %(message)s"
            )
        )
    )
    logger.debug(grey(f"{message}"))
    logger.handlers[0].setFormatter(logging.Formatter(default_logger_format))


def file(caller):
    return caller.filename


def file_spaces(caller):
    return " " * (filename_length - len(f"{file(caller)}"))


def file_elipsed(caller):
    file_name = file(caller)
    if len(file_name) > filename_length:
        return "…" + file_name[(len(file_name) - filename_length + 1) :]
    return file_name


def INFO(message, stack=0, format="None"):
    c = caller(stack + 2)
    logger = logging.getLogger()
    file = file_elipsed(c)
    spaces = " " * (func_name_length - len(c.function))
    spaces_2 = " " * (line_no_length - len(f"{c.lineno}"))
    file_spaces = " " * (filename_length - len(f"{file}"))
    if format == "small":
        pre = f"{file_spaces}{file_elipsed(c)}{spaces_2}{c.lineno} %(levelname){levelname_length}s | "
    elif format == "xs":
        pre = ""
    else:
        pre = f"GMT %(asctime)s {spaces}{func_name_elipsed(c)}() {file_spaces}{file_elipsed(c)}{spaces_2}{c.lineno} %(levelname){levelname_length}s | "
    logger.handlers[0].setFormatter(logging.Formatter(grey(pre) + "%(message)s"))
    logger.info((f"{message}"))
    logger.handlers[0].setFormatter(logging.Formatter(default_logger_format))


def INFO_MULTILINE(message, stack=0):
    for l in message.split("\n"):
        INFO(l, stack + 1)


def INFO_JSON(obj, stack=0, title=None):
    if isinstance(title, str):
        pre = title + " = "
    else:
        pre = ""
    INFO_MULTILINE(pre + json.dumps(obj, indent=4), stack + 1)


def SUCCESS(message, stack=0):
    INFO(green(message), stack + 1)


def WARNING(message):
    level = "WARNING"
    c = caller()
    logger = logging.getLogger()
    spaces = " " * (func_name_length - len(c.function))
    spaces_2 = " " * (line_no_length - len(f"{c.lineno}"))
    spaces_3 = " " * (levelname_length - len(level))
    logger.handlers[0].setFormatter(
        logging.Formatter(
            grey(
                f'GMT %(asctime)s {spaces}{func_name_elipsed(c)}() {file_spaces(c)}{file_elipsed(c)}{spaces_2}{c.lineno} {spaces_3}{yellow(level)} {grey("|")} %(message)s'
            )
        )
    )
    logger.error(yellow(f"{message}"))
    logger.handlers[0].setFormatter(logging.Formatter(default_logger_format))


WARN = WARNING


def ERROR(message):
    level = "ERROR"
    c = caller()
    logger = logging.getLogger()
    spaces = " " * (func_name_length - len(c.function))
    spaces_2 = " " * (line_no_length - len(f"{c.lineno}"))
    spaces_3 = " " * (levelname_length - len(level))
    logger.handlers[0].setFormatter(
        logging.Formatter(
            grey(
                f'GMT %(asctime)s {spaces}{func_name_elipsed(c)}() {file_spaces(c)}{file_elipsed(c)}{spaces_2}{c.lineno} {spaces_3}{red(level)} {grey("|")} %(message)s'
            )
        )
    )
    logger.error(red(f"{message}"))
    logger.handlers[0].setFormatter(logging.Formatter(default_logger_format))


def func_name_elipsed(caller):
    if len(caller.function) > func_name_length:
        return caller.function[: (func_name_length - 1)] + "…"
    return caller.function


def wtf(message):
    c = caller()
    level = "WTF"
    logger = logging.getLogger()
    spaces = " " * (func_name_length - len(c.function))
    spaces_2 = " " * (line_no_length - len(f"{c.lineno}"))
    logger.handlers[0].setFormatter(
        logging.Formatter(
            grey(
                f'GMT %(asctime)s {spaces}{func_name_elipsed(c)}() {file_spaces(c)}{file(c)}{spaces_2}{c.lineno}     {red(level)} {grey("|")} %(message)s'
            )
        )
    )
    logger.error(green(f"{message}"))
    logger.handlers[0].setFormatter(logging.Formatter(default_logger_format))


WTF = wtf
