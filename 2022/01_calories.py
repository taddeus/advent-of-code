#!/usr/bin/env python3
import sys
from heapq import nlargest

def calories_per_elf(lines):
    cal = 0
    for line in lines:
        if line == '\n':
            yield cal
            cal = 0
        else:
            cal += int(line)
    yield cal

top3 = nlargest(3, calories_per_elf(sys.stdin))
print(top3[0])
print(sum(top3))
