#!/usr/bin/env python3
import sys
from functools import reduce
from operator import add, mul

def parse(f):
    lines = f.readlines()
    indices, ops = zip(*((i, (add, mul)['+*'.index(char)])
                         for i, char in enumerate(lines.pop())
                         if char in '+*'))
    indices += (len(lines[-1]),)
    for i, op in enumerate(ops):
        start, end = indices[i:i + 2]
        nums = tuple(line[start:end - 1] for line in lines)
        yield op, nums

def transpose(nums):
    return tuple(int(''.join(n)) for n in zip(*nums))

ops = list(parse(sys.stdin))
print(sum(reduce(op, map(int, nums)) for op, nums in ops))
print(sum(reduce(op, transpose(nums)) for op, nums in ops))
