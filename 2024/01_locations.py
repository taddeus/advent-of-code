#!/usr/bin/env python3
import sys
from collections import Counter

left, right = zip(*(map(int, line.split()) for line in sys.stdin))
print(sum(abs(r - l) for l, r in zip(sorted(left), sorted(right))))
rcounts = Counter(right)
print(sum(l * rcounts[l] for l in left))
