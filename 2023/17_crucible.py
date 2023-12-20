#!/usr/bin/env python3
import sys
from heapq import heappop, heappush

def traverse(grid, minn, maxn):
    maxy = len(grid) - 1
    maxx = len(grid[0]) - 1
    right = 0, 0, (1, 0), 1
    down = 0, 0, (0, 1), 1
    dists = {right: 0, down: 0}
    work = [(0, right), (0, down)]

    while work:
        dist, key = heappop(work)
        x, y, direction, n = key
        if x == maxx and y == maxy:
            return dist
        if dist == dists[key]:
            prevdx, prevdy = direction
            for nbdir in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                dx, dy = nbdir
                nx, ny = nb = x + dx, y + dy
                if 0 <= nx <= maxx and 0 <= ny <= maxy and \
                        ((dx != -prevdx) if dx else (dy != -prevdy)) and \
                        (n < maxn if nbdir == direction else n >= minn):
                    nbdist = dist + grid[ny][nx]
                    nbkey = nx, ny, nbdir, (n * (nbdir == direction) + 1)
                    if nbdist < dists.get(nbkey, 1000000):
                        dists[nbkey] = nbdist
                        heappush(work, (nbdist, nbkey))

grid = [list(map(int, line.rstrip())) for line in sys.stdin]
print(traverse(grid, 1, 3))
print(traverse(grid, 4, 10))
