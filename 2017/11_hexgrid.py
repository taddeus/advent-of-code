#!/usr/bin/env python3
import sys
from math import ceil

steps = {
    'nw': (-1, -.5),
    'n':  ( 0, -1.),
    'ne': ( 1, -.5),
    'sw': (-1,  .5),
    's':  ( 0,  1.),
    'se': ( 1,  .5),
}

def walk(route):
    x = y = 0
    for step in route:
        dx, dy = steps[step]
        x += dx
        y += dy
        yield x, y

def dist(x, y):
    x = abs(x)
    y = abs(y)
    return x + ceil(y - x * .5) if y > x else x

# part 1
route = sys.stdin.readline().rstrip().split(',')
d = [dist(x, y) for x, y in walk(route)]
print(d[-1])
print(max(d))
