#!/usr/bin/env python3
import sys
from functools import partial
from itertools import chain, permutations, starmap

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

def antinodes1(w, h, x, y, dx, dy):
    if 0 <= x + dx < w and 0 <= y + dy < h:
        yield x + dx, y + dy

def antinodes2(w, h, x, y, dx, dy):
    while 0 <= x < w and 0 <= y < h:
        yield x, y
        x += dx
        y += dy

antennas, w, h = parse(sys.stdin)
pairs = list(subtract_pairs(antennas))
print(len(set(chain.from_iterable(starmap(partial(antinodes1, w, h), pairs)))))
print(len(set(chain.from_iterable(starmap(partial(antinodes2, w, h), pairs)))))
