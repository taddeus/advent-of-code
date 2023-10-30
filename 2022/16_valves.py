#!/usr/bin/env python3
import sys
from functools import reduce
from heapq import heappop, heappush
from itertools import chain, product, tee
from operator import or_

def parse(line):
    _, node, _, _, flow, _, _, _, _, nbs = line.split(' ', 9)
    return node, int(flow[5:-1]), nbs.rstrip().split(', ')

def bestcase(graph, opened, time, actors):
    # each minute each actor opens the closed valve with the highest flow rate
    unopened = sorted((rate for i, rate, _ in graph.values()
                      if not opened & (1 << i)), reverse=True)
    times = chain.from_iterable(zip(*tee(range(time, 0, -1), actors)))
    return sum(rate * t for rate, t in zip(unopened, times))

def move(graph, pos, opened, time):
    i, rate, nbs = graph[pos]
    mask = 1 << i
    if rate and not opened & mask:
        yield pos, rate * time, mask
    elif not nbs:
        yield pos, 0, 0
    for nb in nbs:
        yield nb, 0, 0

def open_valves(graph, time, actors):
    work = [(0, time, ('AA',) * actors, 0, 0)]
    best = {}
    all_opened = reduce(or_, (1 << i for i, rate, _ in graph.values() if rate))

    while work:
        _, t, pos, opened, released = heappop(work)
        if t < 2 or opened == all_opened:
            return released
        t -= 1

        for moves in product(*(move(graph, p, opened, t) for p in pos)):
            newpos, newflow, newopen = zip(*moves)
            masks = list(filter(None, newopen))
            # don't open the same valve with multiple actors
            if len(masks) == len(set(masks)):
                newreleased = released + sum(newflow)
                newopened = opened | reduce(or_, newopen)
                potential = newreleased + bestcase(graph, newopened, t, actors)
                key = newpos, newopened
                if best.get(key, 0) < potential:
                    best[key] = potential
                    heappush(work, (-potential, t, newpos, newopened, newreleased))

graph = {valve: (i, rate, nbs)
         for i, (valve, rate, nbs) in enumerate(map(parse, sys.stdin))}
print(open_valves(graph, 30, 1))
print(open_valves(graph, 26, 2))
