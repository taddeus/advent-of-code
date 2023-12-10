#!/usr/bin/env python3
import sys
import re
from functools import reduce
from math import ceil, sqrt
from operator import mul

def wins(time, distance):
    # invariant: hold * (time - hold) > distance
    # solve: -hold^2 + time*hold - distance = 0
    #        hold = (time +- sqrt(time^2 - 4 * distance)) / 2
    #             = (time +- d) / 2
    # solution: (time - d) / 2 < hold < (time + d) / 2
    d = sqrt(time ** 2 - 4 * distance)
    return int((time + d) / 2) - ceil((time - d) / 2) + 1 - 2 * (d % 1 == 0)

times, distances = (re.findall(r'\d+', line) for line in sys.stdin)
print(reduce(mul, (wins(int(t), int(d)) for t, d in zip(times, distances))))
print(wins(int(''.join(times)), int(''.join(distances))))
