#!/usr/bin/env python3
import sys
from collections import defaultdict
from itertools import repeat

def parse(line):
    (x1, y1), (x2, y2) = (part.split(',') for part in line.split(' -> '))
    return int(x1), int(y1), int(x2), int(y2)

def coords(a, b, c, d, diagonal):
    if a == b:
        yield from repeat(a, abs(d - c) + 1)
    elif diagonal or c == d:
        delta = -1 if a > b else 1
        yield from range(a, b + delta, delta)

def overlaps(lines, diagonal):
    grid = defaultdict(int)
    for x1, y1, x2, y2 in lines:
        allx = coords(x1, x2, y1, y2, diagonal)
        ally = coords(y1, y2, x1, x2, diagonal)
        for x, y in zip(allx, ally):
            grid[(x, y)] += 1
    return sum(n > 1 for n in grid.values())

lines = list(map(parse, sys.stdin))
print(overlaps(lines, False))
print(overlaps(lines, True))
