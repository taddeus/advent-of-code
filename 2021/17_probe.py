#!/usr/bin/env python3
import sys
import re
from itertools import islice
from operator import or_
from functools import reduce

def xsteps(dx, lo, hi):
    x = steps = 0
    while x <= hi and dx:
        x += dx
        steps += 1
        dx -= 1
        if lo <= x <= hi:
            if dx:
                yield steps
            else:
                yield from range(steps, 300)

def ysteps(dy, lo, hi):
    y = steps = 0
    while y >= lo:
        y += dy
        dy -= 1
        steps += 1
        if lo <= y <= hi:
            yield steps

def bucketize(values, keys):
    buckets = {}
    for value in values:
        for key in keys(value):
            buckets.setdefault(key, []).append(value)
    return buckets

def sim(x1, x2, y1, y2):
    ix = bucketize(range(1000), lambda dx: xsteps(dx, x1, x2))

    for dy in range(y1, 200):
        for steps in ysteps(dy, y1, y2):
            for dx in set(ix.get(steps, [])):
                yield dx, dy

def maxy(vy):
    return 0 if vy < 0 else vy * (vy + 1) // 2

x1, x2, y1, y2 = map(int, re.findall(r'-?\d+', sys.stdin.readline()))
velocities = list(sim(x1, x2, y1, y2))
print(max(maxy(vy) for vx, vy in velocities))
print(len(velocities))
