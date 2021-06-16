class formattings:
    ENDC =          '\033[0m'
    GREY =          '\033[90m'
    RED =           '\033[91m'
    GREEN =         '\033[92m'
    YELLOW =        '\033[93m'
    BLUE =          '\033[94m'
    PINK =          '\033[95m'
    LIGHT_BLUE =    '\033[96m'
    MAGENTA =       '\033[35m'
    CYAN =          '\033[36m'
def grey(message):
    return f"{formattings.GREY}{message}{formattings.ENDC}"
def blue(message):
    return f"{formattings.BLUE}{message}{formattings.ENDC}"
def green(message):
    return f"{formattings.GREEN}{message}{formattings.ENDC}"
def red(message):
    return f"{formattings.RED}{message}{formattings.ENDC}"
def yellow(message):
    return f"{formattings.YELLOW}{message}{formattings.ENDC}"
def light_blue(message):
    return f"{formattings.LIGHT_BLUE}{message}{formattings.ENDC}"
def pink(message):
    return f"{formattings.PINK}{message}{formattings.ENDC}"
def magenta_light(message):
    return f"{formattings.PINK}{message}{formattings.ENDC}"
def magenta(message):
    return f"{formattings.MAGENTA}{message}{formattings.ENDC}"
s4 = ' '*4
