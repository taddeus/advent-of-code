#!/usr/bin/env python3
import sys

DXDY = {'^': [(0, -1)], 'v': [(0, 1)], '<': [(-1, 0)], '>': [(1, 0)],
        '.': [(0, -1), (0, 1), (-1, 0), (1, 0)]}

def parse(inp):
    graph = {}
    lines = inp.split()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '#':
                graph[(x, y)] = nbs = {}
                for dx, dy in DXDY[lines[y][x]]:
                    nx, ny = nb = x + dx, y + dy
                    if 0 <= ny < len(lines) and lines[ny][nx] != '#':
                        nbs[nb] = 1
    for xy in [xy for xy, nbs in graph.items() if len(nbs) == 2]:
        (left, left_dist), (right, right_dist) = graph.pop(xy).items()
        left_nbs = graph[left]
        if xy in left_nbs:
            left_nbs[right] = left_nbs.pop(xy) + right_dist
        right_nbs = graph[right]
        if xy in right_nbs:
            right_nbs[left] = right_nbs.pop(xy) + left_dist
    return graph

def longest_path(graph):
    start = next(iter(graph))  # python 3.8 guarantees insertion order
    end = next(reversed(graph))
    def dfs(xy, dist, vis):
        if xy == end:
            yield dist
        for nb, nbdist in graph[xy].items():
            if nb not in vis:
                yield from dfs(nb, dist + nbdist, vis | {nb})
    return max(dfs(start, 0, {start}))

inp = sys.stdin.read()
print(longest_path(parse(inp)))
print(longest_path(parse(inp.translate(str.maketrans('<>^v', '....')))))
