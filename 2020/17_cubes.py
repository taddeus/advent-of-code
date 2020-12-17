#!/usr/bin/env python3
import sys
from collections import defaultdict

def parse(f):
    for y, line in enumerate(f):
        for x, cube in enumerate(line.rstrip()):
            if cube == '#':
                yield x, y, 0, 0

def neighbors(coord, extra_dim):
    x, y, z, w = coord
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dw in (-1, 0, 1) if extra_dim else (0,):
                    if dx or dy or dz or dw:
                        yield x + dx, y + dy, z + dz, w + dw

def changes(active, extra_dim):
    inactive = defaultdict(int)
    for coord in active:
        active_nbs = 0
        for nb in neighbors(coord, extra_dim):
            if nb in active:
                active_nbs += 1
            else:
                inactive[nb] += 1
        if active_nbs not in (2, 3):
            yield coord, False

    for coord, active_nbs in inactive.items():
        if active_nbs == 3:
            yield coord, True

def cycle(active, n, extra_dim):
    active = set(active)
    for i in range(n):
        for coord, activate in list(changes(active, extra_dim)):
            (active.add if activate else active.remove)(coord)
    return len(active)

active = list(parse(sys.stdin))
print(cycle(active, 6, False))
print(cycle(active, 6, True))
