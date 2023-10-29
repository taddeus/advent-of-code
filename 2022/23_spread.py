#!/usr/bin/env python3
import sys
from collections import Counter, deque

def add(a, b):
    xa, ya = a
    xb, yb = b
    return xa + xb, ya + yb

def spread(elves):
    directions = deque([
        ((-1, -1), (0, -1), (1, -1)),
        ((-1, 1), (0, 1), (1, 1)),
        ((-1, -1), (-1, 0), (-1, 1)),
        ((1, -1), (1, 0), (1, 1)),
    ])
    while True:
        proposals = {}
        for xy in elves:
            accessible = [all(add(xy, d) not in elves for d in deltas)
                          for deltas in directions]
            proposals[xy] = xy if sum(accessible) in (0, 4) \
                            else add(xy, directions[accessible.index(True)][1])
        if all(src == dst for src, dst in proposals.items()):
            break
        counts = Counter(proposals.values())
        elves = {b if counts[b] == 1 else a for a, b in proposals.items()}
        yield elves
        directions.append(directions.popleft())

def progress(elves):
    minx = min(x for x, y in elves)
    maxx = max(x for x, y in elves)
    miny = min(y for x, y in elves)
    maxy = max(y for x, y in elves)
    return (maxx - minx + 1) * (maxy - miny + 1) - len(elves)

elves = {(x, y)
         for y, line in enumerate(sys.stdin)
         for x, c in enumerate(line.strip())
         if c == '#'}
seq = spread(elves)

for i in range(10): elves = next(seq)
print(progress(elves))

for i, elves in enumerate(seq): pass
print(i + 12)
