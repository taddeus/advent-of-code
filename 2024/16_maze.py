#!/usr/bin/env python3
import sys
from heapq import heappop, heappush

grid = [line.rstrip() for line in sys.stdin]
start = next((x, y) for y, row in enumerate(grid)
            for x, cell in enumerate(row) if cell == 'S')
end = next((x, y) for y, row in enumerate(grid)
        for x, cell in enumerate(row) if cell == 'E')
work = [(0, (start,), 1, 0)]
best_costs = {(*start, 1, 0): 0}
best_end_cost = 0
best_seats = set()

while work:
    cost, path, dx, dy = heappop(work)
    x, y = pos = path[-1]
    if pos == end:
        best_seats |= {*path}
        best_end_cost = cost
    elif not best_end_cost or cost < best_end_cost:
        for cost, x, y, dx, dy in (
            (cost + 1, x + dx, y + dy, dx, dy),  # straight
            (cost + 1000, x, y, dy, -dx),        # left
            (cost + 1000, x, y, -dy, dx),        # right
        ):
            pos = x, y, dx, dy
            if grid[y][x] != '#' and best_costs.get(pos, cost + 1) >= cost:
                best_costs[pos] = cost
                heappush(work, (cost, path + ((x, y),), dx, dy))

print(best_end_cost)
print(len(best_seats))
