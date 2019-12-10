#!/usr/bin/env python3
import sys
from collections import Counter
from operator import itemgetter

# part 1
w, h = 25, 6
pix = [int(c) for c in sys.stdin.readline().rstrip()]
counter = min((Counter(pix[i:i + w * h]) for i in range(0, len(pix), w * h)),
              key=itemgetter(0))
print(counter[1] * counter[2])

# part 2
img = [0] * (w * h)
for start in reversed(range(0, len(pix), w * h)):
    for i in range(w * h):
        if pix[start + i] < 2:
            img[i] = pix[start + i]

for start in range(0, w * h, w):
    print(''.join(' @'[img[start + i]] for i in range(w)))
