import pathlib


from common.logger import *
from common.format import *
from common.read import *


def short_path(path):
    return path.replace(os.environ["HOME"], "$HOME")


def write(path, content, backup=True):
    dir = path.replace(path.split("/")[-1], "")
    pathlib.Path(dir).mkdir(parents=True, exist_ok=True)
    over = ""
    if os.path.exists(path):
        over = "over"
        if backup:
            backup_(path)
    with open(path, "w") as file:
        DEBUG((f"{over}writing {short_path(path)}"))
        file.write(content)


def backup_(path):
    path_bak = path + ".bak"
    copy(path, path_bak, backup=False)


def copy(source_file, destination_file, backup=True):
    write(destination_file, read(source_file), backup)
