#!/usr/bin/env python3
import sys

tr = str.maketrans('FBLR', '0101')
seats = [int(line.translate(tr), 2) for line in sys.stdin]
lo, hi = min(seats), max(seats)
print(hi)
print(int((lo + (hi - lo) / 2) * (len(seats) + 1)) - sum(seats))
