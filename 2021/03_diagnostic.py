#!/usr/bin/env python3
import sys

def common(diag, i):
    return int(sum(n >> i & 1 for n in diag) / len(diag) + .5)

def rating(diag, width, flip_common):
    i = width - 1
    while len(diag) > 1:
        expected = common(diag, i) ^ flip_common
        diag = [n for n in diag if n >> i & 1 == expected]
        i -= 1
    return diag[0]

diag = [int(line, 2) for line in sys.stdin]
width = max(n.bit_length() for n in diag)

gamma = sum(common(diag, i) << i for i in range(width))
epsilon = sum((1 - common(diag, i)) << i for i in range(width))
print(gamma * epsilon)

oxygen = rating(diag, width, True)
co2_scrub = rating(diag, width, False)
print(oxygen * co2_scrub)
