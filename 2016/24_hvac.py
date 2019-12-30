#!/usr/bin/env python3
import sys
from collections import deque
from itertools import chain, permutations

def read_grid(f):
    rows = [line.rstrip() for line in f]
    return list(chain.from_iterable(rows)), len(rows[0])

def shortest_paths(grid, w):
    def bfs(start):
        dists = [0] * nlocs
        work = deque([(start, 0)])
        explored = {start}
        while work:
            loc, dist = work.popleft()

            node = grid[loc]
            if node.isdigit():
                dists[int(node)] = dist

            for nb in (loc - 1, loc + 1, loc - w, loc + w):
                if grid[nb] != '#' and nb not in explored:
                    explored.add(nb)
                    work.append((nb, dist + 1))
        return dists

    nlocs = max(int(x) for x in grid if x.isdigit()) + 1
    return [bfs(grid.index(str(i))) for i in range(nlocs)]

def visit_steps(dists, back):
    dists = shortest_paths(grid, w)
    best = 100000000
    for path in permutations(range(1, len(dists))):
        total = 0
        prev = 0
        for loc in path:
            total += dists[prev][loc]
            prev = loc
        if back:
            total += dists[prev][0]
        best = min(best, total)
    return best


grid, w = read_grid(sys.stdin)
dists = shortest_paths(grid, w)
print(visit_steps(dists, False))
print(visit_steps(dists, True))
