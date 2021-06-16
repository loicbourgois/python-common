import pathlib


from common.logger import *
from common.format import *


def read(path):
    with open(path, 'r') as file:
        # INFO(light_blue(f"reading {path}"))
        return file.read()
