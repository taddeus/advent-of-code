#!/usr/bin/env python3
import sys

tr = str.maketrans('FBLR', '0101')
seats = sorted(int(line.translate(tr), 2) for line in sys.stdin)
print(max(seats))
print(next(s + 1 for i, s in enumerate(seats[:-1]) if seats[i + 1] == s + 2))
