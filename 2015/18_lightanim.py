#!/usr/bin/env python3
import sys

def parse(f):
    data = f.read().rstrip()
    w = data.index('\n') + 2
    pad = [False] * (w + 1)
    grid = pad + [c == '#' for c in data.replace('\n', '..')] + pad
    return grid, w

def animate(grid, w, steps, broken_corners):
    nboff = (-w - 1, -w, -w + 1,
                 -1,          1,
              w - 1,  w,  w + 1)
    corners = (w + 1, 2 * w - 2, -2 * w + 1, -w - 2) \
              if broken_corners else ()

    h = len(grid) // w
    prev = [False] * len(grid)
    grid = [l for l in grid]

    for i in corners:
        grid[i] = True

    for step in range(steps):
        prev, grid = grid, prev

        for y in range(1, h - 1):
            for x in range(1, w - 1):
                i = y * w + x
                on = prev[i]
                nbon = sum(int(prev[i + off]) for off in nboff)
                grid[i] = nbon == 3 or (on and nbon == 2)

        for i in corners:
            grid[i] = True

    return sum(map(int, grid))

grid, w = parse(sys.stdin)
print(animate(grid, w, 100, False))
print(animate(grid, w, 100, True))
