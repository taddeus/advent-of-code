#!/usr/bin/env python3
import sys

UP, DOWN, LEFT, RIGHT = DIRECTIONS = (0, -1), (0, 1), (-1, 0), (1, 0)
CONN = {'|': (UP, DOWN), '-': (LEFT, RIGHT), '7': (LEFT, DOWN),
        'J': (LEFT, UP), 'L': (UP, RIGHT), 'F': (RIGHT, DOWN)}

def parse(inp):
    graph = {}
    for y, line in enumerate(inp):
        for x, char in enumerate(line.rstrip()):
            graph[(x, y)] = [(x + dx, y + dy) for dx, dy in CONN.get(char, ())]
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

def inner(border):
    b = len(border)
    x, y = zip(*border)
    area = abs(sum(x[i] * y[(i + 1) % b] - y[i] * x[(i + 1) % b]
                   for i in range(b))) // 2  # Shoelace formula
    return area - b // 2 + 1  # Pick's theorem

border = loop(*parse(sys.stdin))
print(len(border) // 2)
print(inner(border))
