"""
Simple, pretty ping wrapper (for *nix).

Colorizes ping results and displays as a bar graph on a log scale.
"""

import argparse
import datetime
import sys
import time
from multiprocessing import Process
from multiprocessing import Queue

from pyng import asyncping
from pyng import color
from pyng import settings
from pyng import utils

assert sys.version_info >= (3, 6, 0)


HEADER = '|'.join(
    '{:<{}}'.format(
        utils.column_to_timescale_header(i),
        settings.WIDTH,
    )
    for i in range(settings.COLUMNS)
)
SUBHEADER = '+'.join(
    '-' * settings.WIDTH for i in range(settings.COLUMNS)
)


def graph(num):
    """
    Graphs the given ping result on a log scale.
    (must be 0 <= num <= 999999)

    Returns a single output row (no color, Unicode).
    """
    if not 0 <= num <= 999999:
        print("Got ping outside range [0, 999999]")
        return

    num = int(num)
    num_str = str(num)
    digits = len(num_str)
    first_digit = int(num_str[0])

    row = [settings.BLANK * settings.WIDTH] * settings.COLUMNS
    for i in range(digits - 1):
        blocks = settings.FILL * settings.WIDTH
        row[i] = blocks

    row[digits - 1] = '{:{}<{}}'.format(
        settings.HEAD * first_digit,
        settings.BLANK,
        settings.WIDTH,
    )

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
    print(row)


def loop(queue, host, pings):
    """Wait for ping results and display them prettily"""
    loops = 0
    while pings != 0:
        result = queue.get()

        # header, for context
        if not loops % settings.PINGS_PER_HEADER:
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
