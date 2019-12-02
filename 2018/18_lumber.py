#!/usr/bin/env python3
import sys

OPEN, TREE, LUMB = range(3)

trans = {'.': OPEN, '|': TREE, '#': LUMB}
initial = []
for line in sys.stdin:
    w = len(line) + 1
    initial += [OPEN, *(trans[c] for c in line.rstrip()), OPEN]
pad = [OPEN] * w
initial = pad + initial + pad
h = len(initial) // w

def simulate(minutes):
    prev = list(initial)
    grid = [0] * len(prev)

    for minute in range(minutes):
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                i = y * w + x
                cell = prev[i]

                counts = [0, 0, 0]
                for d in (-w - 1, -w, -w + 1, -1, 1, w - 1, w, w + 1):
                    counts[prev[i + d]] += 1

                if cell == OPEN and counts[TREE] >= 3:
                    cell = TREE
                elif cell == TREE and counts[LUMB] >= 3:
                    cell = LUMB
                elif cell == LUMB and (not counts[LUMB] or not counts[TREE]):
                    cell = OPEN

                grid[i] = cell

        counts = [0, 0, 0]
        for x in grid:
            counts[x] += 1
        yield counts[TREE] * counts[LUMB], hash(tuple(grid))

        prev, grid = grid, prev

# part 1
for val, ident in simulate(10):
    last = val
print(last)

# part 2
def find_pattern(n):
    seen = []
    for minute, result in enumerate(simulate(n)):
        for i in range(len(seen) - 1, -1, -1):
            if seen[i] == result:
                return minute, tuple(zip(*seen[i:]))[0]
        seen.append(result)

n = 1000000000
minute, pattern = find_pattern(n)
print(pattern[(n - minute - 1) % len(pattern)])
