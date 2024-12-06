#!/usr/bin/env python3
import sys

grid = [line.rstrip() for line in sys.stdin]
h = len(grid)
w = len(grid[0])
guard = next((x, y) for y in range(h) for x in range(w) if grid[y][x] == '^')
obstacles = {(x, y) for y in range(h) for x in range(w) if grid[y][x] == '#'}

def walk(x, y, dx, dy, obstacles):
    while 0 <= x < w and 0 <= y < h:
        if (x, y) in obstacles:
            x -= dx
            y -= dy
            dx, dy = -dy, dx
        else:
            yield (x, y), (dx, dy)
            x += dx
            y += dy

def loops(path, visited):
    vis = {(x, y, dx, dy) for (x, y), d in visited.items() for dx, dy in d}
    for pos in path:
        if pos in vis:
            return True
        vis.add(pos)
    return False

def add_obstacle(gx, gy, obstacles):
    positions = set()
    visited = {}
    for xy, d in walk(gx, gy, 0, -1, obstacles):
        if xy not in visited and xy not in positions and \
                loops(walk(*xy, *d, obstacles | {xy}), visited):
            positions.add(xy)
        visited.setdefault(xy, set()).add(d)
    return positions

print(len(set(xy for xy, _ in walk(*guard, 0, -1, obstacles))))
print(len(add_obstacle(*guard, obstacles)))
