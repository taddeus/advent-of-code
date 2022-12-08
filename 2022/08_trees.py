#!/usr/bin/env python3
import sys

def parse(f):
    first = next(f).rstrip()
    grid = list(map(int, first))
    for line in f:
        grid.extend(map(int, line.rstrip()))
    return grid, len(first)

def visible(grid, size):
    vis = [False] * len(grid)

    def walk(start, step):
        prev = -1
        for i in range(start, start + step * size, step):
            tree = grid[i]
            if tree > prev:
                vis[i] = True
                prev = tree

    for i in range(size):
        walk(i, size)
        walk(len(grid) - i - 1, -size)
        walk(i * size, 1)
        walk((i + 1) * size - 1, -1)

    return sum(vis)

def score(grid, size, i):
    def walk(step, stop):
        vis = 0
        for j in range(i + step, stop, step):
            vis += 1
            if grid[j] >= grid[i]:
                break
            j += step
        return vis

    return walk(1, i + size - i % size) \
         * walk(-1, i - i % size - 1) \
         * walk(size, len(grid)) \
         * walk(-size, -1)

grid, size = parse(sys.stdin)
print(visible(grid, size))
print(max(score(grid, size, i) for i in range(len(grid))))
