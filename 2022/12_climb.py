#!/usr/bin/env python3
import sys
from heapq import heappop, heappush

def parse(content):
    grid = [ord(x) - ord('a') for x in content if x != '\n']
    w = content.find('\n')
    src = grid.index(ord('S') - ord('a'))
    dst = grid.index(ord('E') - ord('a'))
    grid[src] = 0
    grid[dst] = 25
    return grid, w, src, dst

def closest_starts(grid, w, dst):
    h = len(grid) // w
    def neighbors(i):
        y, x = divmod(i, w)
        if x > 0: yield i - 1
        if x < w - 1: yield i + 1
        if y > 0: yield i - w
        if y < h - 1: yield i + w

    dist = [1 << 31] * len(grid)
    dist[dst] = 0
    worklist = [(0, dst)]

    while worklist:
        udist, u = heappop(worklist)
        if udist == dist[u]:
            for v in neighbors(u):
                if grid[u] <= grid[v] + 1:
                    alt = dist[u] + 1
                    if alt < dist[v]:
                        dist[v] = alt
                        heappush(worklist, (alt, v))
    return dist

grid, w, src, dst = parse(sys.stdin.read())
dist = closest_starts(grid, w, dst)
print(dist[src])
print(min(d for elev, d in zip(grid, dist) if not elev))
