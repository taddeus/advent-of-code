#!/usr/bin/env python3
import sys
from intcode import read_program, run

def paint(firmware, color):
    robot = run(firmware, lambda: color, 1000)
    painted = set()
    white = set()
    x = y = 0
    dx, dy = 0, -1
    for make_white in robot:
        painted.add((x, y))
        (white.add if make_white else white.discard)((x, y))
        dx, dy = (-dy, dx) if next(robot) else (dy, -dx)
        x += dx
        y += dy
        color = int((x, y) in white)
    return white, len(painted)

def draw(coords):
    xmin = min(x for x, y in coords)
    xmax = max(x for x, y in coords)
    ymin = min(y for x, y in coords)
    ymax = max(y for x, y in coords)

    grid = [[0] * (xmax - xmin + 1) for y in range(ymin, ymax + 1)]
    for x, y in coords:
        grid[y - ymin][x - xmin] = 1

    for row in grid:
        print(''.join(' @'[c] for c in row))

firmware = read_program(sys.stdin)
white, npainted = paint(firmware, 0)
print(npainted)
white, npainted = paint(firmware, 1)
draw(white)
