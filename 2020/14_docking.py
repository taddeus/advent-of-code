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

def run(program, v2):
    mem = {}
    and_mask = or_mask = 0
    fluct = []
    for is_mask, a, b in program:
        if v2 and is_mask:
            and_mask = ~a & ~b
            or_mask = b
            fluct = [i for i in range(36) if (a >> i) & 1]
        elif v2:
            for bits in product((0, 1), repeat=len(fluct)):
                fluct_bits = (bit << i for bit, i in zip(bits, fluct))
                fluct_mask = reduce(or_, fluct_bits, 0)
                mem[a & and_mask | or_mask | fluct_mask] = b
        elif is_mask:
            and_mask = a
            or_mask = b
        else:
            mem[a] = b & and_mask | or_mask
    return sum(mem.values())

program = list(parse(sys.stdin))
print(run(program, False))
print(run(program, True))
