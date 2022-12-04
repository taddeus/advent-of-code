#!/usr/bin/env python3
import sys
import re

pairs = [tuple(map(int, re.split('[,-]', line))) for line in sys.stdin]
print(sum(a >= c and b <= d if d - c > b - a else c >= a and d <= b
          for a, b, c, d in pairs))
print(sum(d >= a if c < a else b >= c for a, b, c, d in pairs))
