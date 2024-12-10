#!/usr/bin/env python3
import sys
from collections import Counter

def trail_ends(grid, headx, heady):
    h = len(grid)
    w = len(grid[0])
    work = [(headx, heady, 0, set())]
    while work:
        x, y, num, visited = work.pop()
        if num == 9:
            yield x, y
        else:
            for nb in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                nx, ny = nb
                if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == num + 1 \
                        and nb not in visited:
                    work.append((nx, ny, num + 1, visited | {nb}))

grid = [list(map(int, line[:-1])) for line in sys.stdin]
trails = [Counter(trail_ends(grid, x, y))
          for y, row in enumerate(grid)
          for x, num in enumerate(row)
          if num == 0]
print(sum(map(len, trails)))
print(sum(sum(t.values()) for t in trails))
