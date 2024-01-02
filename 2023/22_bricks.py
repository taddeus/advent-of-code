#!/usr/bin/env python3
import sys
from functools import reduce

def parse(line):
    left, right = line.rstrip().split('~')
    xs, ys, zs = map(int, left.split(','))
    xe, ye, ze = map(int, right.split(','))
    return [(x, y, z) for x in range(xs, xe + 1)
                      for y in range(ys, ye + 1)
                      for z in range(zs, ze + 1)]

def drop(i, brick, stack):
    air = 0
    while not any(z - air == 1 or (x, y, z - air - 1) in stack
                  for x, y, z in brick):
        air += 1
    for x, y, z in brick:
        stack[(x, y, z - air)] = i
        base = stack.get((x, y, z - air - 1), i)
        if base != i:
            yield base

def disintegrate(bricks):
    bricks = sorted(bricks, key=lambda brick: min(z for x, y, z in brick))
    stack = {}
    supports = [set(drop(i, brick, stack)) for i, brick in enumerate(bricks)]
    dom = [set(range(len(bricks))) for _ in bricks]
    lens = [0] * len(dom)
    while any(len(d) != l for d, l in zip(dom, lens)):
        lens = list(map(len, dom))
        dom = [{i} | reduce(set.intersection, map(dom.__getitem__, supp))
               if supp else {i} for i, supp in enumerate(supports)]
    for i in range(len(dom)):
        yield sum(i in d for j, d in enumerate(dom) if j != i)

would_fall = list(disintegrate(map(parse, sys.stdin)))
print(would_fall.count(0))
print(sum(would_fall))
