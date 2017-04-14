"""
Display utilities
"""


def column_to_timescale_header(col):
    if col >= 3:
        return "1{}s".format('0' * (col - 3))
    else:
        return "1{}ms".format('0' * col)
