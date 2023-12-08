#!/usr/bin/env python3
import sys
from itertools import cycle, islice
from math import lcm

def follow(instructions, graph, cur, end):
    for step, inst in enumerate(cycle(instructions)):
        if cur.endswith(end):
            return step
        cur = graph[cur][inst]

inst = ['LR'.index(c) for c in next(sys.stdin).rstrip()]
graph = {l[:3]: (l[7:10], l[12:15]) for l in islice(sys.stdin, 1, None)}
print(follow(inst, graph, 'AAA', 'ZZZ'))
print(lcm(*(follow(inst, graph, n, 'Z') for n in graph if n.endswith('A'))))
