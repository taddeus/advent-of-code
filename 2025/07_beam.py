#!/usr/bin/env python3
import sys

def visit(xy):
    x, y = xy
    if xy in paths:
        return 0
    if y == len(grid):
        paths[xy] = 1
        return 0
    if grid[y][x] == '^':
        left = x - 1, y + 1
        right = x + 1, y + 1
        splits = 1 + visit(left) + visit(right)
        paths[xy] = paths[left] + paths[right]
        return splits
    splits = visit((x, y + 1))
    paths[xy] = paths[(x, y + 1)]
    return splits

grid = sys.stdin.read().split()
start = grid[0].index('S'), 0
paths = {}
print(visit(start))
print(paths[start])
