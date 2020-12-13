#!/usr/bin/env python3
import sys
from functools import reduce
from itertools import combinations
from operator import mul

def group(expenses, n):
    for group in combinations(expenses, n):
        if sum(group) == 2020:
            return reduce(mul, group)

expenses = list(map(int, sys.stdin))
print(group(expenses, 2))
print(group(expenses, 3))
