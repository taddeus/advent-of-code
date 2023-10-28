#!/usr/bin/env python3
import sys
from collections import deque

def mix(numbers, times):
    buf = deque(range(len(numbers)))
    for _ in range(times):
        for i in range(len(buf)):
            buf.rotate(-buf.index(i))
            buf.rotate(-numbers[buf.popleft()])
            buf.appendleft(i)
    buf.rotate(-buf.index(numbers.index(0)))
    return sum(numbers[buf[i % len(buf)]] for i in (1000, 2000, 3000))

numbers = list(map(int, sys.stdin))
print(mix(numbers, 1))
print(mix([n * 811589153 for n in numbers], 10))
