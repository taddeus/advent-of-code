#!/usr/bin/env python3
import sys
from functools import lru_cache

def mul_diffs(adapters):
    seq = [0] + sorted(adapters)
    diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)] + [3]
    return diffs.count(1) * diffs.count(3)

def arrangements(adapters):
    @lru_cache(maxsize=4)
    def ways(jo):
        return jo in exists and \
               (jo <= 3) + ways(jo - 1) + ways(jo - 2) + ways(jo - 3)
    exists = set(adapters)
    return ways(max(adapters))

adapters = list(map(int, sys.stdin))
print(mul_diffs(adapters))
print(arrangements(adapters))
