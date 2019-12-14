#!/usr/bin/env python3
import sys
from collections import defaultdict

def read_graph(f):
    graph = {'ORE': (1, {})}
    for line in f:
        lhs, rhs = line.strip().split(' => ')
        noutp, outp = rhs.split()
        assert outp not in graph
        edges = {}
        for inp in lhs.split(', '):
            ninp, inp = inp.split()
            edges[inp] = int(ninp)
        graph[outp] = int(noutp), edges
    return graph

def ore_needed(reactions, fuel):
    def produce(outp, amount):
        from_stash = min(amount, stash[outp])
        stash[outp] -= from_stash
        amount -= from_stash
        noutp, inputs = reactions[outp]
        multiplier = amount // noutp + bool(amount % noutp)
        for inp, ninp in inputs.items():
            produce(inp, ninp * multiplier)
        stash[outp] += noutp * multiplier - amount
        produced[outp] += amount

    stash = defaultdict(int)
    produced = defaultdict(int)
    produce('FUEL', fuel)
    return produced['ORE']

def fuel_with_ore(reactions, ore):
    fuel = 0
    step = ore
    while step:
        while ore_needed(reactions, fuel) < ore:
            fuel += step
        fuel -= step
        step //= 2
    return fuel

reactions = read_graph(sys.stdin)
print(ore_needed(reactions, 1))
print(fuel_with_ore(reactions, 1000000000000))
