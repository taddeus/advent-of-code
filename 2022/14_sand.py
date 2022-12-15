#!/usr/bin/env python3
import sys

def parse(f):
    for line in f:
        path = [tuple(map(int, xy.split(','))) for xy in line.split(' -> ')]
        for i in range(len(path) - 1):
            (xs, ys), (xe, ye) = sorted(path[i:i + 2])
            for x in range(xs, xe + 1):
                for y in range(ys, ye + 1):
                    yield x, y

def fill(obstacles, bottom, void):
    def drop():
        x = 500
        for y in range(void):
            for dx in (0, -1, 1):
                if (x + dx, y + 1) not in obstacles and y + 1 != bottom:
                    x += dx
                    break
            else:
                return x, y

    pos = drop()
    while pos and pos != (500, 0):
        obstacles.add(pos)
        pos = drop()
    return len(obstacles)

obstacles = set(parse(sys.stdin))
rock = len(obstacles)
bottom = max(y for x, y in obstacles) + 2
print(fill(obstacles, bottom, bottom - 1) - rock)
print(fill(obstacles, bottom, bottom + 1) - rock + 1)
