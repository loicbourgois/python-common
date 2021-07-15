import multiprocessing


from common.logger import *
from common.format import *
from common.timeit import *


from common.write import short_path


stdouts = {}


# @timeit
def runcmd(
    command: str, quiet=False, shell=False, parallel=False, dir=None, format=None
):
    return runcmd_list(
        command.split(" "),
        quiet,
        shell=shell,
        parallel=parallel,
        dir=dir,
        format=format,
    )


def runcmd_parallel(command: str):
    return runcmd_list(command.split(" "), parallel=True)


def runcmd_list(
    command: list, quiet=False, shell=False, parallel=False, dir=None, format=None
):

    if not quiet:
        for line in " ".join(command).split("\n"):
            dir_str = ""
            if dir:
                dir_str = grey(f" # in {dir}")
            line = short_path("$ " + line + dir_str)
            if parallel:
                line = f"[{os.getpid()}]" + line
            INFO(line, format=format)

    def stream_process(process, command_id):
        go = process.poll() is None
        for line in process.stdout:
            l = os.linesep.join([s for s in line.decode("UTF8").splitlines() if s])
            if not quiet:
                if parallel:
                    INFO((f"  [{os.getpid()}] {l}"), format=format)
                else:
                    INFO(("  " + l), format=format)
            stdouts[command_id].append(l)
        return go

    command_id = str(uuid.uuid4())
    stdouts[command_id] = []
    process = subprocess.Popen(
        command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=dir
    )
    while stream_process(process, command_id):
        time.sleep(0.1)
    assert (
        process.returncode == 0
    ), f"invalid returncode: expected 0, got {process.returncode} - command: {command}"
    return stdouts[command_id]


def runcmds_parallel(cmds):
    ps = start_cmds_parallel(cmds)
    join_cmds_parallel(ps)


def start_cmds_parallel(cmds):
    cmd = cmds[0]
    ps = []
    for cmd in cmds:
        p = multiprocessing.Process(target=runcmd_parallel, args=(cmd,))
        p.start()
        ps.append(p)
    return ps


def join_cmds_parallel(ps):
    for p in ps:
        p.join()
