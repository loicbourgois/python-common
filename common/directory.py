import os


from common.logger import *


def make_sure_path_exists(path):
    if not os.path.exists(path):
        INFO(f"{path} does not exist")
        INFO(f"creating {path}")
        os.makedirs(path, exist_ok=True)
    assert os.path.isdir(path), ERROR(f"{path} is a file, not a directory")
