#!/usr/bin/env python3
import sys
from functools import cache
from itertools import pairwise

NUMERIC = '789' '456' '123' ' 0A'
DIRECTIONAL = ' ^A' '<v>'

def walk(keypad, x, y, path):
    i = y * 3 + x
    for direction in path:
        i += (-1, 1, -3, 3)['<>^v'.index(direction)]
        yield keypad[i]

def paths_between(keypad, start, end):
    y1, x1 = divmod(keypad.index(start), 3)
    y2, x2 = divmod(keypad.index(end), 3)
    hor = '<>'[x2 > x1] * abs(x2 - x1)
    ver = '^v'[y2 > y1] * abs(y2 - y1)
    for path in {hor + ver, ver + hor}:
        if ' ' not in walk(keypad, x1, y1, path):
            yield path + 'A'

@cache
def cost_between(keypad, start, end, links):
    return min(cost(DIRECTIONAL, path, links - 1)
               for path in paths_between(keypad, start, end)) if links else 1

@cache
def cost(keypad, keys, links):
    return sum(cost_between(keypad, a, b, links)
               for a, b in pairwise('A' + keys))

def complexity(code, robots):
    return cost(NUMERIC, code, robots + 1) * int(code[:-1])

codes = sys.stdin.read().split()
print(sum(complexity(code, 2) for code in codes))
print(sum(complexity(code, 25) for code in codes))
