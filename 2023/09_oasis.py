#!/usr/bin/env python3
import sys
from itertools import pairwise

def predict(n):
    return n[-1] + predict([r - l for l, r in pairwise(n)]) if any(n) else 0

histories = [list(map(int, line.split())) for line in sys.stdin]
print(sum(map(predict, histories)))
print(sum(predict(h[::-1]) for h in histories))
