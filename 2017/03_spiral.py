#!/usr/bin/env python3
def spiral_coords():
    x = y = 0
    step = 1
    while True:
        for x in range(x + 1, x + step + 1):
            yield x, y
        for y in range(y - 1, y - step - 1, - 1):
            yield x, y
        step += 1
        for x in range(x - 1, x - step - 1, -1):
            yield x, y
        for y in range(y + 1, y + step + 1):
            yield x, y
        step += 1

def spiral_dist(n):
    for i, (x, y) in zip(range(n - 1), spiral_coords()):
        pass
    return abs(x) + abs(y)

# part 1
inp = 277678
print(spiral_dist(inp))

# part 2
w = 100
grid = w * w * [0]
mid = w // 2
grid[mid * w + mid] = 1
neighbour_offsets = (-w - 1, -w, -w + 1, -1, 1, w - 1, w, w + 1)
for x, y in spiral_coords():
    i = (y + mid) * w + (x + mid)
    n = grid[i] = sum(grid[i + nb] for nb in neighbour_offsets)
    if n >= inp:
        print(n)
        break
