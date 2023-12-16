#!/usr/bin/env python3
import sys

def energize(grid, x, y, dx, dy, visited=None):
    visited = {} if visited is None else visited
    while 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        directions = visited.setdefault((x, y), [])
        if (dx, dy) in directions:
            break
        directions.append((dx, dy))
        cell = grid[y][x]
        if cell in '/\\':
            dx, dy = (dy, -dx) if (dx if cell == '/' else dy) else (-dy, dx)
        elif cell == '-' and dy:
            energize(grid, x + 1, y, 1, 0, visited)
            dx, dy = -1, 0
        elif cell == '|' and dx:
            energize(grid, x, y + 1, 0, 1, visited)
            dx, dy = 0, -1
        x += dx
        y += dy
    return len(visited)

def energies(grid):
    w = len(grid[0])
    h = len(grid)
    for x in range(w):
        yield energize(grid, x, 0, 0, 1)
        yield energize(grid, x, h - 1, 0, -1)
    for y in range(h):
        yield energize(grid, 0, y, 1, 0)
        yield energize(grid, w - 1, y, -1, 0)

grid = [line.rstrip() for line in sys.stdin]
print(energize(grid, 0, 0, 1, 0))
print(max(energies(grid)))
