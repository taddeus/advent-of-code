#!/usr/bin/env python3
import re
import sys

def parse(f):
    for i, line in enumerate(f):
        nr, size, time, pos = map(int, re.findall(r'\d+', line))
        assert nr == i + 1
        assert time == 0
        yield size, pos

def is_range(seq):
    return all(seq[i] - seq[i - 1] == 1 for i in range(1, len(seq)))

def button_time(discs):
    sizes, positions = zip(*discs)
    desired = tuple(-(delay + 1) % size for delay, size in enumerate(sizes))
    time = 0
    while positions != desired:
        positions = tuple((p + 1) % s for s, p in zip(sizes, positions))
        time += 1
    return time

discs = list(parse(sys.stdin))
print(button_time(discs))
print(button_time(discs + [(11, 0)]))
