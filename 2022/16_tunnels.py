#!/usr/bin/env python3
import sys
from functools import lru_cache

def parse(line):
    _, node, _, _, flow, _, _, _, _, nbs = line.split(' ', 9)
    return node, int(flow[5:-1]), nbs.rstrip().split(', ')

def open_valves(graph, time, helpers):
    @lru_cache(maxsize=None)
    def travel(opened, pos, t, helpers):
        if t == 0:
            return travel(opened, 'AA', time, helpers - 1) if helpers else 0

        i, rate, nbs = graph[pos]
        mask = 1 << i
        best = 0
        if rate and opened & mask == 0:
            rest = travel(opened | mask, pos, t - 1, helpers)
            best = max(best, rate * (t - 1) + rest)
        for nb in nbs:
            best = max(best, travel(opened, nb, t - 1, helpers))
        return best

    return travel(0, 'AA', time, helpers)

graph = {valve: (i, rate, nbs)
         for i, (valve, rate, nbs) in enumerate(map(parse, sys.stdin))}
print(open_valves(graph, 30, 0))
print(open_valves(graph, 26, 1))
