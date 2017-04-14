
from __future__ import unicode_literals


def _color(string, ansi):
    """Colors the given string with the given ANSI color index."""
    return "\x1b[0;{}m{}\x1b[0m".format(ansi, string)


def green(string):
    return _color(string, 32)


def yellow(string):
    return _color(string, 33)


def red(string):
    return _color(string, 31)


def black(string):
    return _color(string, 30)


def color(string, index):
    """Colors the given string based on list position (ANSI)."""
    if index in (0, 1):
        return green(string)
    elif index == 2:
        return yellow(string)
    elif index == 3:
        return red(string)
    else:
        return black(string)
