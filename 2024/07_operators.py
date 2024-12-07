#!/usr/bin/env python3
import sys
from functools import reduce
from itertools import product
from operator import add, mul

def parse(line):
    result, operands = line.split(': ', 1)
    return int(result), tuple(map(int, operands.split()))

def solve(result, nums, operators):
    return any(reduce(lambda a, b: next(ops)(a, b), nums) == result
               for ops in map(iter, product(operators, repeat=len(nums) - 1)))

def concat(a, b):
    b_digits = 1
    while b_digits <= b:
        b_digits *= 10
    return a * b_digits + b

expr = list(map(parse, sys.stdin))
print(sum(res for res, op in expr if solve(res, op, (add, mul))))
print(sum(res for res, op in expr if solve(res, op, (add, mul, concat))))
