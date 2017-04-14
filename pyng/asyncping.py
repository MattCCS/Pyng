"""
Thread to asynchronously run `ping` and yield (queue) parsed times
"""

import re
import subprocess


TIME_REGEX = r"""time=([0-9\.]+) ms"""


def fetch_times(queue, host, pings=-1):
    """
    Runs ping() in the background, parsing and
    appending its results to a buffer.
    """

    ping = subprocess.Popen(['ping', host], stdout=subprocess.PIPE)

    # this lets us set PINGS to -1 to run forever
    while pings != 0:
        line = ping.stdout.readline().strip()

        if line and not line.startswith("PING"):
            try:
                num = int(float(re.search(TIME_REGEX, line).group(1)))
            except AttributeError:
                num = -1  # probably a timeout

            queue.put(num)
            pings -= 1
