#!/usr/bin/env python3
import sys

def read_wire(f):
    return [(x[0], int(x[1:])) for x in f.readline().split(',')]

def trace(wire):
    multipliers = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
    x = y = steps = 0
    visited = {}
    for direction, distance in wire:
        dx, dy = multipliers[direction]
        for i in range(distance):
            x += dx
            y += dy
            steps += 1
            visited.setdefault((x, y), steps)
    return visited

path1 = trace(read_wire(sys.stdin))
path2 = trace(read_wire(sys.stdin))
intersections = set(path1) & set(path2)
print(min(abs(x) + abs(y) for x, y in intersections))
print(min(path1[i] + path2[i] for i in intersections))
