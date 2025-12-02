#!/usr/bin/env python3
import sys

zeroes = passes = 0
dial = 50
for line in sys.stdin:
    delta = -1 if line[0] == 'L' else 1
    amount = int(line[1:])
    for _ in range(amount):
        dial = (dial + delta) % 100
        passes += dial == 0
    zeroes += dial == 0

print(zeroes)
print(passes)
