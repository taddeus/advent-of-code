#!/usr/bin/env python3
import sys
import re
from collections import namedtuple
from itertools import combinations

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

nodes = list(parse(sys.stdin))
print(sum(1 for pair in viable_pairs(nodes)))
