#!/usr/bin/env python3
import sys
from collections import defaultdict, deque
from itertools import combinations
from math import atan2, gcd, pi

def read_asteroids(f):
    for y, line in enumerate(f):
        for x, c in enumerate(line):
            if c == '#':
                yield x, y

def angle(dx, dy):
    return pi / 2 - atan2(dx, dy)

def raytrace(asteroids):
    xmax = max(x for x, y in asteroids)
    ymax = max(y for x, y in asteroids)
    exists = set(asteroids)
    visible = defaultdict(dict)

    def trace(x, y, dx, dy):
        x += dx
        y += dy
        while 0 <= x <= xmax and 0 <= y <= ymax:
            if (x, y) in exists:
                return x, y
            x += dx
            y += dy

    for a, b in combinations(asteroids, 2):
        ax, ay = a
        bx, by = b
        dx = bx - ax
        dy = by - ay
        div = gcd(dx, dy)
        if trace(ax, ay, dx // div, dy // div) == b:
            visible[a][angle(dx, dy)] = b
            visible[b][angle(-dx, -dy)] = a

    return visible

def shoot_laser(visible, station):
    targets = deque(sorted(visible[station].items()))
    while targets:
        angle, target = targets.popleft()
        yield target
        replacement = visible[target].get(angle, None)
        if replacement is not None:
            targets.append((angle, replacement))

# part 1
asteroids = list(read_asteroids(sys.stdin))
visible = raytrace(asteroids)
station = max(visible, key=lambda x: len(visible[x]))
print(len(visible[station]))

# part 2
targets = shoot_laser(visible, station)
for i in range(200):
    x, y = next(targets)
print(x * 100 + y)
