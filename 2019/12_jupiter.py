#!/usr/bin/env python3
from itertools import chain, combinations, islice
from math import gcd

def cmp(a, b):
    return (a > b) - (a < b)

def abssum(i):
    return sum(map(abs, i))

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def sim(axis):
    pos = list(axis)
    vel = [0] * len(pos)
    index_pairs = tuple(combinations(range(len(pos)), 2))
    while True:
        for i, j in index_pairs:
            diff = cmp(pos[j], pos[i])
            vel[i] += diff
            vel[j] -= diff
        for i, v in enumerate(vel):
            pos[i] += v
        yield pos, vel

def energy_after(moons, steps):
    x, y, z = zip(*moons)
    axes = next(islice(zip(sim(x), sim(y), sim(z)), steps - 1, steps))
    pos, vel = zip(*axes)
    return sum(abssum(p) * abssum(v) for p, v in zip(zip(*pos), zip(*vel)))

def axis_cycle(axis):
    seen = {}
    for step, (pos, vel) in enumerate(sim(axis)):
        prevstep = seen.setdefault(tuple(pos + vel), step)
        if prevstep != step:
            return step - prevstep

def find_cycle(moons):
    x, y, z = zip(*moons)
    return lcm(lcm(axis_cycle(x), axis_cycle(y)), axis_cycle(z))

moons = [(3, 15, 8), (5, -1, -2), (-10, 8, 2), (8, 4, -5)]
print(energy_after(moons, 1000))
print(find_cycle(moons))
