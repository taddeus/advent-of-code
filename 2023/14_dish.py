#!/usr/bin/env python3
import sys
import re

def rotate(rocks):
    return tuple(''.join(rocks[y][x] for y in range(len(rocks) - 1, -1, -1))
                 for x in range(len(rocks[0])))

def roll(rocks):
    for row in rocks:
        subs = 1
        while subs:
            row, subs = re.subn(r'(\.+)(O+)', r'\2\1', row)
        yield row

def load(rocks):
    return sum((len(rocks) - y) * row.count('O') for y, row in enumerate(rocks))

def cycle(rocks, n):
    rocks = rotate(rotate(rotate(rocks)))
    seen = {rocks: 0}
    for i in range(1, n + 1):
        for _ in range(4):
            rocks = rotate(tuple(roll(rocks)))
        phase = i - seen.setdefault(rocks, i)
        if phase:
            return cycle(rotate(rocks), (n - i) % phase)
    return rotate(rocks)

rocks = tuple(line.rstrip() for line in sys.stdin)
print(load(rotate(tuple(roll(rotate(rotate(rotate(rocks))))))))
print(load(cycle(rocks, 1000000000)))
