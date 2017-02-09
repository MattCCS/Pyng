"""
Simple, pretty ping wrapper (for *nix).

Colorizes ping results and displays as a bar graph on a log scale.
"""

from __future__ import unicode_literals

import re
import time
import argparse
import datetime
import threading
import subprocess


COLUMNS = 6
WIDTH = 9  # <--- do not change -- we use a log scale, so we range from 0 to 9.

def ms_s(i):
    if i >= 3:
        return "1{}s".format('0' * (i - 3))
    else:
        return "1{}ms".format('0' * i)


HEADER = '|'.join('{:<9}'.format(ms_s(i)) for i in range(COLUMNS))
SUBHEADER = '+'.join('-' * 9 for i in range(COLUMNS))

BLANK = '.'
HEAD = u'\u2588'
FILL = HEAD



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
    if index == 0:
        return green(string)
    elif index in (1, 2):
        return yellow(string)
    elif index == 3:
        return red(string)
    else:
        return black(string)



def graph(num):
    """
    Graphs the given ping result on a log scale.
    (must be 0 <= num <= 999999)

    Returns a single output row (no color, Unicode).
    """

    num = int(num)
    num_str = str(num)
    digits = len(num_str)
    first_digit = int(num_str[0])

    row = [BLANK * WIDTH] * COLUMNS
    for i in range(digits - 1):
        blocks = FILL * WIDTH
        row[i] = blocks

    row[digits - 1] = u'{:{}<{}}'.format(HEAD * first_digit, BLANK, WIDTH)

    return '|'.join(row)



RUN = True
PINGS = None
HOST = None
TIMES = []  # milliseconds
TIME_REGEX = r"""time=([0-9\.]+) ms"""


def fetch_times():
    """
    Runs ping() in the background, parsing and
    appending its results to a buffer.
    """

    global PINGS
    global RUN

    ping = subprocess.Popen(['ping', HOST], stdout=subprocess.PIPE)

    while PINGS != 0:
        line = ping.stdout.readline().strip()
        if line and not line.startswith("PING"):
            try:
                num = int(float(re.search(TIME_REGEX, line).group(1)))
                TIMES.append(num)
            except AttributeError:
                TIMES.append(-1)  # probably a timeout
            PINGS -= 1

    RUN = False



def parse_args():
    """Parses and saves command-line arguments."""
    global PINGS
    global HOST

    parser = argparse.ArgumentParser()
    parser.add_argument('host',  default='www.google.com', nargs='?')
    parser.add_argument('-p', '--pings', default=-1, type=int)
    args = parser.parse_args()

    PINGS = args.pings
    HOST = args.host



def loop():
    """Main loop.  Waits for ping results and displays them prettily."""

    loops = 0
    while TIMES or RUN:
        try:
            res = TIMES.pop(0)

            # header, for context
            if not loops % 20:
                print('')
                print(datetime.datetime.now().strftime("%D %H:%M:%S"))
                print("Pinging: {} ({})".format(HOST, "{} left".format(PINGS) if PINGS > 0 else "forever"))
                print(HEADER)
                print(SUBHEADER)

            if res > 0:
                row = graph(res)
                blocks = row.split('|')
                row = '|'.join(color(e, i) for (i, e) in enumerate(blocks))
                print(row.encode('utf-8'))  # <--- unicode sandwich.
            else:
                print("TIMEOUT!")

            loops += 1

        except IndexError:
            pass  # no new data

        # if we get a ton of results in rapid successon, we will
        # update the screen quickly (~100/sec) until we catch up
        time.sleep(0.01)


def main():
    """Gets arguments, starts ping, and begins loop."""

    parse_args()

    ping_thread = threading.Thread(target=fetch_times)
    ping_thread.start()

    loop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        PINGS = 0
    except:
        PINGS = 0
        raise