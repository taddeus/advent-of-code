#!/usr/bin/env python3
import sys
from itertools import combinations
spreadsheet = [list(map(int, line.split())) for line in sys.stdin]
print(sum(max(row) - min(row) for row in spreadsheet))
print(sum(div for row in spreadsheet
              for a, b in combinations(row, 2)
              for div, rem in (divmod(a, b), divmod(b, a))
              if rem == 0))
