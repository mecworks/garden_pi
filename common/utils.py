# Some useful functions

import time


def timestamp():
    """
    Return our standard timestamp, the unix epic seconds, accurate to 4 decimal places.

    :return: str
    """
    return '{0:.4f}'.format(time.time())


def format_float(f):
    fmt = '{0:.3f}'
    if f is None:
        return " "
    else:
        return fmt.format(f)


def conv_s2hms(seconds, short=False):
    """
    Converts seconds to hours, minutes and seconds.

    :param seconds: The time in seconds to use
    :type seconds: int

    :return: str
    """
    seconds = int(seconds)
    hours = seconds / 3600
    seconds -= 3600 * hours
    minutes = seconds / 60
    seconds -= 60 * minutes
    if hours == 0 and short is True:
        return "%02d:%02d" % (minutes, seconds)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


console_colors = {
    'norm': '\033[0m',
    'bold': '\033[1m',
    'red': '\033[31m',
    'green': '\033[32m',
    'orange': '\033[33m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'purple': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
}


# noinspection PyPep8Naming
def printColor(msg, color, newline=True):
    """
    Prints a string in color

    :param msg: Text to colorize
    :type msg: str
    :param color: Color, one of those listed in helpers.console_colors
    :type color: str
    :param newline: Whether or not to terminate string with a carriage return
    :type newline: bool

    :return: None (print to console)
    """
    nl = os.linesep if newline else ''
    sys.stdout.write('%s%s' % (colorize(msg, color), nl))
    sys.stdout.flush()


def colorize(msg, color):
    """
    Colorize a string and return the string

    :param msg: Text to colorize
    :type msg: str
    :param color: Color, one of those listed in helpers.console_colors
    :type color: str

    :return: str
    """
    return '%s%s%s' % (console_colors[color], msg, console_colors['norm'])

