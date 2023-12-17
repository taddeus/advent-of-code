#!/usr/bin/env python3
import sys

def spread(grid, w, i):
    yield range(i + 1, i - i % w + w)
    yield range(i - 1, i - i % w - 1, -1)
    yield range(i + w, len(grid), w)
    yield range(i - w, -1, -w)

def visible(grid, w):
    return sum(any(all(grid[j] < tree for j in d) for d in spread(grid, w, i))
               for i, tree in enumerate(grid))

def score(grid, w, i):
    def walk(direction):
        vis = 0
        for j in direction:
            vis += 1
            if grid[j] >= grid[i]:
                break
        return vis
    right, left, down, up = map(iter, spread(grid, w, i))
    return walk(right) * walk(left) * walk(down) * walk(up)

inp = sys.stdin.read()
w = inp.index('\n')
grid = [int(n) for n in inp if n != '\n']
print(visible(grid, w))
print(max(score(grid, w, i) for i, tree in enumerate(grid)))
