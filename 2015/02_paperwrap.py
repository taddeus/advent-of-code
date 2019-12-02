#!/usr/bin/env python3
import sys
boxes = [tuple(map(int, line.split('x'))) for line in sys.stdin]
print(sum(2 * (l * w + w * h + h * l) + min(l * w, w * h, h * l)
          for l, w, h in boxes))
print(sum(2 * min(l + w, w + h, h + l) + l * w * h
          for l, w, h in boxes))
