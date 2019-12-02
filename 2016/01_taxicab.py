#!/usr/bin/env python3
import sys


def walk(instructions):
    x = y = 0
    dx = 0
    dy = -1
    yield x, y

    for turn, distance in instructions:
        if turn == 'L':
            dy, dx = -dx, dy
        elif turn == 'R':
            dy, dx = dx, -dy

        for i in range(distance):
            x += dx
            y += dy
            yield x, y


def dist(x, y):
    return abs(x) + abs(y)


instructions = [(w[0], int(w[1:])) for w in sys.stdin.readline().split(', ')]

# part 1
for pos in walk(instructions):
    pass
print(dist(*pos))

# part 2
visited = set()
for pos in walk(instructions):
    if pos in visited:
        break
    visited.add(pos)
print(dist(*pos))
