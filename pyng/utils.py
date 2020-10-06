"""
Display utilities
"""


def column_to_timescale_header(col):
    if col >= 3:
        return "1{0}-9{0}s".format('0' * (col - 3))
    else:
        return "1{0}-9{0}ms".format('0' * col)
