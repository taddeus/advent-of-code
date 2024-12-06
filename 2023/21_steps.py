#!/usr/bin/env python3
import sys
from collections import deque

def bfs(grid):
    h = len(grid)
    w = len(grid[0])
    start = next((x, y) for y in range(h) for x in range(w) if grid[y][x] == 'S')
    visited = {start: 0}
    work = deque([(start, 0)])
    while work:
        (x, y), steps = work.popleft()
        for nb in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            nx, ny = nb
            if 0 <= nx < w and 0 <= ny < h:
                if grid[ny][nx] != '#' and nb not in visited:
                    visited[nb] = steps + 1
                    work.append((nb, steps + 1))
    return visited

def reachable_in_26501365_steps(min_dists):
    # https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
    n = (26501365 - 131 // 2) // 131  # w = h = 131
    even = odd = even_corners = odd_corners = 0
    for dist in min_dists.values():
        is_odd = dist % 2
        even += 1 - is_odd
        odd += is_odd
        if dist > 65:
            even_corners += 1 - is_odd
            odd_corners += is_odd
    whole_squares = (n + 1) ** 2 * odd + n * n * even
    corners = (n + 1) * odd_corners + n * even_corners
    return whole_squares - corners

min_dists = bfs(sys.stdin.read().split())
print(sum(dist % 2 == 0 and dist <= 64 for xy, dist in min_dists.items()))
print(reachable_in_26501365_steps(min_dists))
