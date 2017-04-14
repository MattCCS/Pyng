Pyng
====
A pure-Python ping wrapper for pretty and fast network assessment.

Requirements
------------
- Python 2.7+
- pip or pip3 (to install)
- Mac/Linux

Installation
------------
Run ``pip install pyng3``, or run ``pip3 install pyng3``

How to Use
----------
Run ``pyng`` or ``pyng3``.  You can pass a host (defaults to www.google.com),
and -p for a finite number of pings.

Features
--------
- colorized output for easy visualization
- log scale to handle all ranges of latency
- specify host and number of pings (-1 is infinite)
- < 80 characters wide!
- Tested with Python 2.7 and Python 3.6

Un-Features
-----------
- Not tested on Linux
- No support for specifying ping rate
