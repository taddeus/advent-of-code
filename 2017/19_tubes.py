#!/usr/bin/env python3
import sys

grid = sys.stdin.read().split('\n')
y = 0
x = grid[0].index('|')
dy = 1
dx = 0
seen = ''
steps = 0

while grid[y][x] != ' ':
    y += dy
    x += dx
    steps += 1
    cell = grid[y][x]

    if cell == '+':
        if dy and grid[y][x - 1] != ' ':
            dy, dx = 0, -1
        elif dy and grid[y][x + 1] != ' ':
            dy, dx = 0, 1
        elif dx and grid[y - 1][x] != ' ':
            dy, dx = -1, 0
        elif dx and grid[y + 1][x] != ' ':
            dy, dx = 1, 0
    elif ord('A') <= ord(cell) <= ord('Z'):
        seen += cell

print(seen)
print(steps)
