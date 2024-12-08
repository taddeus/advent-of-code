#!/usr/bin/env python3
import sys
from itertools import chain, permutations

def parse(f):
    antennas = {}
    for y, line in enumerate(f):
        for x, char in enumerate(line[:-1]):
            if char != '.':
                antennas.setdefault(char, []).append((x, y))
    return antennas, x + 1, y + 1

def subtract_pairs(antennas):
    for locs in antennas.values():
        for (xa, ya), (xb, yb) in permutations(locs, 2):
            yield xb, yb, xb - xa, yb - ya

def draw_line(x, y, dx, dy, w, h):
    while 0 <= x < w and 0 <= y < h:
        yield x, y
        x += dx
        y += dy

antennas, w, h = parse(sys.stdin)
antinodes = [list(draw_line(*vec, w, h)) for vec in subtract_pairs(antennas)]
print(len(set(a[1] for a in antinodes if len(a) > 1)))
print(len(set(chain.from_iterable(antinodes))))
