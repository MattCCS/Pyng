
from __future__ import unicode_literals


# change these carefully... we use a log scale, so WIDTH ranges from 0 to 9
COLUMNS = 6
WIDTH = 9

PINGS_PER_HEADER = 20
BLANK = '.'

# defines the body and right-most end of the bar graph
# for example, if FILL = "-" and HEAD = ">", you will see "----->"
FILL = '\u2588'  # U+2588 = solid block
HEAD = '\u2588'
