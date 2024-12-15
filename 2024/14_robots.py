#!/usr/bin/env python3
import sys
import re
from itertools import islice

W = 101
H = 103

def walk(robots):
    positions, velocities = zip(*((r[:2], r[2:]) for r in robots))
    while True:
        positions = [((x + dx) % W, (y + dy) % H)
                     for (x, y), (dx, dy) in zip(positions, velocities)]
        yield positions

def safety(positions):
    quadrants = [0, 0, 0, 0]
    midx = W // 2
    midy = H // 2
    for x, y in positions:
        if x != midx and y != midy:
            quadrants[(x > midx) + 2 * (y > midy)] += 1
    a, b, c, d = quadrants
    return a * b * c * d

positions = walk(tuple(map(int, re.findall(r'-?\d+', line)))
                 for line in sys.stdin)
for step in range(1, 101):
    pos = next(positions)
print(safety(pos))
s = ''
while 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' not in s:
    pos = set(next(positions))
    s = ''.join('.X'[(x, y) in pos] for y in range(H) for x in range(W))
    step += 1
print(step)
