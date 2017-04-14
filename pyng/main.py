"""
Simple, pretty ping wrapper (for *nix).

Colorizes ping results and displays as a bar graph on a log scale.
"""

from __future__ import unicode_literals

import time
import argparse
import datetime
import threading
from multiprocessing import Process
from multiprocessing import Queue

from pyng import asyncping
from pyng import color
from pyng import utils


# change these carefully... we use a log scale, so WIDTH ranges from 0 to 9
COLUMNS = 6
WIDTH = 9

PINGS_PER_HEADER = 20
BLANK = '.'
HEAD = u'\u2588'
FILL = HEAD

HEADER = '|'.join(
    '{:<{}}'.format(utils.column_to_timescale_header(i), WIDTH)
    for i in range(COLUMNS)
)
SUBHEADER = '+'.join('-' * WIDTH for i in range(COLUMNS))


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


def parse_args():
    """Parses and saves command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('host',  default='www.google.com', nargs='?')
    parser.add_argument('-p', '--pings', default=-1, type=int)
    return parser.parse_args()


def print_header(host, pings):
    print('')
    print(datetime.datetime.now().strftime("%D %H:%M:%S"))
    print("Pinging: {} ({})".format(host, "{} left".format(pings) if pings > 0 else "forever"))
    print(HEADER)
    print(SUBHEADER)


def print_graph(result):
    row = graph(result)
    blocks = row.split('|')
    row = '|'.join(color.color(e, i) for (i, e) in enumerate(blocks))
    print(row.encode('utf-8'))  # <--- unicode sandwich.


def loop(queue, host, pings):
    """Wait for ping results and display them prettily"""
    loops = 0
    while pings != 0:
        result = queue.get()

        # header, for context
        if not loops % PINGS_PER_HEADER:
            print_header(host, pings)

        if result > 0:
            print_graph(result)
        else:
            print("TIMEOUT!")

        loops += 1
        pings -= 1

        # if we get a ton of results in rapid successon, we will
        # update the screen quickly (~100/sec) until we catch up
        time.sleep(0.01)


def main():
    """Get arguments, start ping, and begin loop"""
    args = parse_args()
    host = args.host
    pings = args.pings

    queue = Queue()

    ping_thread = Process(
        target=asyncping.fetch_times,
        args=(queue, host),
        kwargs={"pings": pings},
    )
    ping_thread.start()

    try:
        loop(queue, host, pings)
    except KeyboardInterrupt:
        print("Closing.")

    ping_thread.terminate()


if __name__ == '__main__':
    main()
