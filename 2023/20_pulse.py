#!/usr/bin/env python3
import sys
from collections import deque
from itertools import count
from math import lcm

def parse(inp):
    graph = {}
    for line in inp:
        src, dst = line.rstrip().split(' -> ')
        outputs = dst.split(', ')
        ty = src[0]
        if ty in '%&':
            src = src[1:]
        prev = graph.get(src, (None, [], None))[1]
        graph[src] = ty, prev, outputs
        for out in outputs:
            graph.setdefault(out, (None, [], []))[1].append(src)
    return graph

def pulse(graph, flipflops, conjunctions):
    work = deque([('button', 'broadcaster', False)])
    while work:
        prev, node, high = work.popleft()
        yield node, high
        ty, inputs, outputs = graph[node]
        if ty == '%':
            if not high:
                flipflops[node] = out = not flipflops.get(node, False)
                work.extend((node, output, out) for output in outputs)
        elif ty == '&':
            state = conjunctions.setdefault(node, {i: False for i in inputs})
            state[prev] = high
            out = not all(state.values())
            work.extend((node, output, out) for output in outputs)
        else:
            work.extend((node, output, high) for output in outputs)

def low_high_counts(graph, times):
    flipflops = {}
    conjunctions = {}
    counts = [0, 0]
    for _ in range(times):
        for _, high in pulse(graph, flipflops, conjunctions):
            counts[high] += 1
    return counts[0] * counts[1]

def pulse_until_rx(graph):
    flipflops = {}
    conjunctions = {}
    sync_nodes = graph[graph['rx'][1][0]][1]
    periods = {}
    for presses in count(1):
        for node, high in pulse(graph, flipflops, conjunctions):
            if not high and node in sync_nodes:
                periods[node] = presses
                if len(periods) == len(sync_nodes):
                    return lcm(*periods.values())

graph = parse(sys.stdin)
print(low_high_counts(graph, 1000))
print(pulse_until_rx(graph))
