import functools
import sys
import json
import time


from common.logger import DEBUG
from common.format import *


def timeit(method):
    @functools.wraps(method)
    def time_it(*args, **kw):
        spaces = ""
        frame = sys._getframe().f_back
        try:
            while frame.f_code.co_name != "<module>":
                frame = frame.f_back
                spaces += "·"
        except:
            pass
        spaces = spaces[(int(len(spaces) / 2)) :]
        args_str = json.dumps(args) + json.dumps(kw)
        l = 80
        if len(args_str) > l:
            args_str = args_str[: l - 3] + "..."
        DEBUG(f"{spaces}{method.__name__}({args_str})")
        t_start = time.time()
        result = method(*args, **kw)
        t_end = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int(te - ts)
        else:
            DEBUG(f"{spaces}{method.__name__}({args_str}) - {(t_end - t_start):2.3f}s")
        return result

    return time_it
