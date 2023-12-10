#!/usr/bin/env python3
import sys
from itertools import chain, pairwise

UP, DOWN, LEFT, RIGHT = DIRECTIONS = (0, -1), (0, 1), (-1, 0), (1, 0)
CONNECTIONS = {
    '|': (UP, DOWN),
    '-': (LEFT, RIGHT),
    '7': (LEFT, DOWN),
    'J': (LEFT, UP),
    'L': (UP, RIGHT),
    'F': (RIGHT, DOWN),
    '.': (),
    'S': (),
}

def parse(inp):
    graph = {}
    for y, line in enumerate(inp):
        for x, char in enumerate(line.rstrip()):
            graph[(x, y)] = [(x + dx, y + dy) for dx, dy in CONNECTIONS[char]]
            if char == 'S':
                sx, sy = start = x, y
    graph[start] = [(sx + dx, sy + dy) for dx, dy in DIRECTIONS
                    if start in graph.get((sx + dx, sy + dy), [])]
    return graph, start

def loop(graph, start):
    path = [start]
    nex = graph[start][0]
    while nex != start:
        path.append(nex)
        nex = next(nb for nb in graph[nex] if nb != path[-2])
    return path

def find_outside(border):
    maxx, maxy = map(max, zip(*border))
    outside = set(chain(((0, y) for y in range(maxy + 1)),
                        ((maxx, y) for y in range(maxy + 1)),
                        ((x, 0) for x in range(maxx + 1)),
                        ((x, maxy) for x in range(maxx + 1)))) - border
    explore = list(outside)
    while explore:
        x, y = explore.pop()
        for dx, dy in DIRECTIONS:
            nx, ny = nb = x + dx, y + dy
            if 0 <= nx <= maxx and 0 <= ny <= maxy and \
                    nb not in outside and nb not in border:
                outside.add(nb)
                explore.append(nb)
    return outside

def area(border):
    scaled = {(2 * x, 2 * y) for x, y in border}
    scaled |= {(ax + bx, ay + by)
               for (ax, ay), (bx, by) in pairwise(chain(border, border[:1]))}
    outside = sum(x % 2 + y % 2 == 0 for x, y in find_outside(scaled))
    maxx, maxy = map(max, zip(*border))
    return (maxx + 1) * (maxy + 1) - outside - len(border)

border = loop(*parse(sys.stdin))
print(len(border) // 2)
print(area(border))
