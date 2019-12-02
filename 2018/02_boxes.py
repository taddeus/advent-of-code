#!/usr/bin/env python3
import sys
from collections import Counter
boxes = [line.rstrip() for line in sys.stdin]

two = three = 0
for box in boxes:
    hist = Counter(box)
    two += int(2 in hist.values())
    three += int(3 in hist.values())
print(two * three)

for box1 in boxes:
    for box2 in boxes:
        dist = 0
        for a, b in zip(box1, box2):
            dist += int(a != b)
        if dist == 1:
            print(''.join(c for c in box1 if c in box2))
            sys.exit(0)
