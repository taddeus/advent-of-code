#!/usr/bin/env python3
import sys
from collections import Counter

# part 1
lines = [line.rstrip() for line in sys.stdin]
print(''.join(Counter(pos).most_common(1)[0][0]
              for pos in zip(*lines)))

# part 2
print(''.join(min((v, k) for k, v in Counter(pos).items())[1]
              for pos in zip(*lines)))
