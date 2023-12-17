#!/usr/bin/env python3
import sys
from heapq import nlargest

top3 = nlargest(3, (sum(map(int, group.split()))
                    for group in sys.stdin.read().split('\n\n')))
print(top3[0])
print(sum(top3))
