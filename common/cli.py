def argv_to_x(*xl, **xd):
    if len(xl) == 0:
        return xd
    else:
        k, v = xl[0].split("=")
        xd.update({k: v})
        return argv_to_x(*xl[1:], **xd)
