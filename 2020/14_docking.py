#!/usr/bin/env python3
import sys
from functools import reduce
from itertools import product
from operator import or_

def parse(f):
    x_tr = str.maketrans('X1', '10')
    for line in f:
        left, right = line.rstrip().split(' = ')
        if left == 'mask':
            x = int(right.translate(x_tr), 2)
            ones = int(right.replace('X', '0'), 2)
            yield True, x, ones
        else:
            yield False, int(left[4:-1]), int(right)

def run_v1(program):
    mem = {}
    and_mask = or_mask = 0
    for is_mask, a, b in program:
        if is_mask:
            and_mask = a
            or_mask = b
        else:
            mem[a] = b & and_mask | or_mask
    return sum(mem.values())

def run_v2(program):
    mem = {}
    fluct_masks = []
    for is_mask, a, b in program:
        if is_mask:
            and_mask = ~(a | b)
            or_mask = b
            fl = [i for i in range(36) if a >> i & 1]
            fluct_masks = [reduce(or_, (b << i for b, i in zip(bits, fl)), 0)
                           for bits in product((0, 1), repeat=len(fl))]
        else:
            for fluct_mask in fluct_masks:
                mem[a & and_mask | or_mask | fluct_mask] = b
    return sum(mem.values())

program = list(parse(sys.stdin))
print(run_v1(program))
print(run_v2(program))
