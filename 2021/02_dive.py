#!/usr/bin/env python3
import sys

DELTA = {'forward': (1, 0), 'up': (0, -1), 'down': (0, 1)}

def parse(line):
    direction, amount = line.split()
    return DELTA[direction], int(amount)

x = y = aimed_y = 0

for (dx, dy), amount in map(parse, sys.stdin):
    x += dx * amount
    y += dy * amount
    aimed_y += dx * y * amount

print(x * y)
print(x * aimed_y)
