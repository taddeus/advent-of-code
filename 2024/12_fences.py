#!/usr/bin/env python3
import sys
from itertools import pairwise

def neighbors(x, y):
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))

def regions(grid):
    h = len(grid)
    w = len(grid[0])
    visited = set()

    def bfs(x, y):
        ty = grid[y][x]
        visited.add((x, y))
        work = [(x, y)]
        while work:
            x, y = work.pop()
            yield x, y
            for nb in neighbors(x, y):
                nx, ny = nb
                if 0 <= nx < w and 0 <= ny < h and \
                        grid[ny][nx] == ty and nb not in visited:
                    visited.add(nb)
                    work.append(nb)

    for y in range(h):
        for x in range(w):
            if (x, y) not in visited:
                yield set(bfs(x, y))

def fences(region):
    for xy in region:
        for nb in neighbors(*xy):
            if nb not in region:
                yield xy, nb

def sides(region):
    indexed = {}
    for (x1, y1), (x2, y2) in fences(region):
        if x1 == x2:
            indexed.setdefault((True, y1, y2), []).append(x1)
        else:
            indexed.setdefault((False, x1, x2), []).append(y1)
    return sum(1 + sum(b - a > 1 for a, b in pairwise(sorted(line)))
               for line in indexed.values())

def perimeter(region):
    return sum(1 for _ in fences(region))

grid = [line[:-1] for line in sys.stdin]
reg = list(regions(grid))
print(sum(len(r) * perimeter(r) for r in reg))
print(sum(len(r) * sides(r) for r in reg))
