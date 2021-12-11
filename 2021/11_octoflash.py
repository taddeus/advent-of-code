#!/usr/bin/env python3
import sys
from itertools import count

def parse(content):
    return list(map(int, content.replace('\n', ''))), content.find('\n')

def flash(grid, w):
    h = len(grid) // w

    def neighbors(i):
        y, x = divmod(i, w)
        if y:
            if x: yield i - w - 1
            yield i - w
            if x < w - 1: yield i - w + 1
        if x: yield i - 1
        if x < w - 1: yield i + 1
        if y < h - 1:
            if x: yield i + w - 1
            yield i + w
            if x < w - 1: yield i + w + 1

    def increase(i):
        grid[i] += 1
        if grid[i] == 10:
            for nb in neighbors(i):
                increase(nb)

    for i in range(len(grid)):
        increase(i)
    flashed = 0
    for i, energy in enumerate(grid):
        if energy > 9:
            flashed += 1
            grid[i] = 0
    return flashed

grid, w = parse(sys.stdin.read())
print(sum(flash(grid, w) for i in range(100)))
print(next(n for n in count(101) if flash(grid, w) == len(grid)))
