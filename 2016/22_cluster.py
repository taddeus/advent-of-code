#!/usr/bin/env python3
import sys
import re
from collections import namedtuple
from itertools import combinations
from heapq import heappop, heappush

Node = namedtuple('Node', 'x, y, size, used, avail')

def parse(f):
    for line in f:
        if line.startswith('/'):
            x, y, size, used, avail, usep = map(int, re.findall(r'\d+', line))
            assert used + avail == size
            yield Node(x, y, size, used, avail)

def viable_pairs(nodes):
    for a, b in combinations(nodes, 2):
        if 0 < a.used <= b.avail:
            yield a, b
        elif 0 < b.used <= a.avail:
            yield b, a

def move_steps(nodes):
    w = max(node.x for node in nodes) + 1
    h = len(nodes) // w

    used = [0] * len(nodes)
    size = [0] * len(nodes)
    for node in nodes:
        i = node.y * w + node.x
        used[i] = node.used
        size[i] = node.size

    def neighbors(i):
        y, x = divmod(i, w)
        if x > 0:
            yield i - 1
        if x < w - 1:
            yield i + 1
        if y > 0:
            yield i - w
        if y < h - 1:
            yield i + w

    def shortest_path(source, dest):
        assert used[source] == 0
        frontier = [(0, source)]
        explored = {source}
        prev = {}
        while frontier:
            dist, u = heappop(frontier)
            if u == dest:
                path = []
                while u != source:
                    path.append(u)
                    u = prev[u]
                path.append(source)
                return path[::-1]
            for v in neighbors(u):
                if v not in explored and v != data and used[v] <= size[u]:
                    heappush(frontier, (dist + 1, v))
                    explored.add(v)
                    prev[v] = u

    def move(src, dst):
        assert dst in neighbors(src)
        assert size[dst] >= used[dst] + used[src]
        used[dst] += used[src]
        used[src] = 0

    empties = set(b for a, b in viable_pairs(nodes))
    assert len(empties) == 1
    empty = empties.pop()
    empty = empty.y * w + empty.x

    data = w - 1
    steps = 0

    while data != 0:
        path = shortest_path(empty, data - 1)
        for i in range(len(path) - 1):
            move(path[i + 1], path[i])
            empty = path[i + 1]
        move(data, empty)
        data, empty = empty, data
        steps += len(path)

    return steps

nodes = list(parse(sys.stdin))
print(sum(1 for pair in viable_pairs(nodes)))
print(move_steps(nodes))
