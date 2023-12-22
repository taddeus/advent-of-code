#!/usr/bin/env python3
import sys
from itertools import accumulate, pairwise

def parse(line):
    direction, distance, color = line.split()
    d = int(distance)
    yield ((d, 0), (0, d), (-d, 0), (0, -d))['RDLU'.index(direction)]
    d = int(color[2:7], 16)
    yield ((d, 0), (0, d), (-d, 0), (0, -d))[int(color[7])]

def dig(steps):
    xy = list(zip(*map(accumulate, zip(*steps))))
    return sum(xa * yb - ya * xb + abs(xb - xa + yb - ya)
               for (xa, ya), (xb, yb) in pairwise(xy + xy[:1])) // 2 + 1

wrong, color = zip(*map(parse, sys.stdin))
print(dig(wrong))
print(dig(color))
