#!/usr/bin/env python3
import sys
from itertools import accumulate, islice, tee

strengths, positions = tee(accumulate(
    int(word) if word[-1].isdigit() else 0
    for word in ('1 ' + sys.stdin.read()).split()))

print(sum((i + 1) * x for i, x in islice(enumerate(strengths), 19, None, 40)))

for row in range(6):
    print(''.join('.#'[abs(next(positions) - col) <= 1] for col in range(40)))
