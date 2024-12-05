#!/usr/bin/env python3
import sys

grid = [line.rstrip() for line in sys.stdin]
w = len(grid[0])
h = len(grid)

def read(x, y, dx, dy, remainder):
    return not remainder or (
        0 <= x < w and
        0 <= y < h and
        grid[y][x] == remainder[0] and
        read(x + dx, y + dy, dx, dy, remainder[1:])
    )

def is_xmas(x, y):
    return sum(read(x, y, dx, dy, 'XMAS')
               for dx in range(-1, 2) for dy in range(-1, 2) if dx or dy)

def is_x_mas(x, y):
    diag1 = grid[y - 1][x - 1] + grid[y][x] + grid[y + 1][x + 1]
    diag2 = grid[y + 1][x - 1] + grid[y][x] + grid[y - 1][x + 1]
    return diag1 in ('MAS', 'SAM') and diag2 in ('MAS', 'SAM')

print(sum(is_xmas(x, y) for y in range(h) for x in range(w)))
print(sum(is_x_mas(x, y) for y in range(1, h - 1) for x in range(1, w - 1)))
