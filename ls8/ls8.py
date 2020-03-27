#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if __name__ == '__main__':
    args = sys.argv
    cpu = CPU()
    if len(args) == 2:
        cpu.load(args[1])
    else:
        cpu.load()
    cpu.run()

