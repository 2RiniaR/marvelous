from datetime import datetime
from enum import Enum


class Color(Enum):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    DEFAULT = '\033[39m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERSE = '\033[07m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_DEFAULT = '\033[49m'
    RESET = '\033[0m'


def colored(message: str, color: Color):
    return color + message + Color.RESET


def get_timespamp(time: datetime):
    return time.strftime("%Y-%m-%d %H:%M:%S.%f")


def write_row(message: str):
    print(message)


def write_debug(message: str):
    prefix = "DEBUG"
    timespamp = get_timespamp(datetime.now())
    output = f'{prefix} ({timespamp}) {message}'
    print(output)


def write_trace(message: str):
    prefix = "TRACE"
    timespamp = get_timespamp(datetime.now())
    output = f'{prefix} ({timespamp}) {message}'
    print(output)


def write_info(message: str):
    prefix = "INFO "
    timespamp = get_timespamp(datetime.now())
    output = f'{prefix} ({timespamp}) {message}'
    print(output)


def write_warning(message: str):
    prefix = "WARN "
    timespamp = get_timespamp(datetime.now())
    output = f'{prefix} ({timespamp}) {message}'
    print(Color.colored(output, Color.YELLOW))


def write_error(message: str):
    prefix = "ERROR"
    timespamp = get_timespamp(datetime.now())
    output = f'{prefix} ({timespamp}) {message}'
    print(Color.colored(output, Color.RED))


def write_fatal(message: str):
    prefix = "FATAL"
    timespamp = get_timespamp(datetime.now())
    output = f'{prefix} ({timespamp}) {message}'
    print(Color.colored(output, Color.BG_MAGENTA))
