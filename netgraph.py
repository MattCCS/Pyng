# encoding: utf-8

# FORM: xxxxxxxxx|xxxxxxxxx|xxxxxxxxx|xxxxxxxxx|...

####################################

HEADER = '|'.join('{:<9}'.format('1' + '0'*i + 'ms') for i in xrange(6))
SUBHEADER = '+'.join('-'*9 for i in xrange(6))

BLANK = '.'
HEAD = u'\u2588'
FILL = HEAD

def graph(num):
    num = int(num)

    s = str(num)
    first = int(s[0])

    L = [BLANK*9] * 6
    for i in xrange(len(s)):
        L[i] = FILL*9

    L[len(s)-1] = u'{:{}<9}'.format(HEAD*first, BLANK)
    
    return '|'.join(L)

####################################

import re
import sys
import time
import datetime
import threading
import subprocess

RUN = True
PINGS = None
HOST = None
TIMES = [] # milliseconds
TIME_REGEX = r"""time=([0-9\.]+) ms"""

def fetch_times():
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
                TIMES.append(-1) # probably a timeout
            PINGS -= 1

    RUN = False

####################################

def parse_args():
    global PINGS
    global HOST

    try:
        PINGS = int(sys.argv[1])
    except IndexError:
        print "Please supply a number of pings to send (-1 is infinite)."
        exit()
    except ValueError:
        print "If you're gonna supply something, make it an integer!"
        exit()

    try:
        HOST = sys.argv[2]
    except IndexError:
        HOST = 'www.google.com'

    print "Pinging: {}".format(HOST)
    print "({})".format("{} times".format(PINGS) if PINGS > 0 else "forever")

####################################

def color(s, n):
    return "\x1b[0;{}m{}\x1b[0m".format(n, s)

def green(s):
    return color(s, 32)

def yellow(s):
    return color(s, 33)

def red(s):
    return color(s, 31)

def black(s):
    return color(s, 30)

def main():

    parse_args()

    t = threading.Thread(target=fetch_times)
    t.start()

    i = 0
    while TIMES or RUN:
        try:
            t = TIMES.pop(0)
            if not i % 20:
                print
                print datetime.datetime.now().strftime("%D %H:%M:%S")
                print HEADER
                print SUBHEADER
            if t > 0:
                g = graph(t).encode('utf-8')
                L = g.split('|')
                g = '|'.join([green(L[0]), yellow(L[1]), yellow(L[2])] + map(red, L[3:-2]) + map(black, L[-2:]))
                print g
            else:
                print "TIMEOUT!"
            i += 1
        except IndexError:
            pass # no new data
        time.sleep(0.01)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        PINGS = 0
    except:
        PINGS = 0
        raise
