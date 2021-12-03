#!/usr/bin/env python3
import sys

def common(diag, i):
    return int(sum(n >> i & 1 for n in diag) / len(diag) + .5)

def gamma(diag, width):
    return sum(common(diag, i) << i for i in range(width))

def epsilon(diag, width):
    return sum((1 - common(diag, i)) << i for i in range(width))

def rating(diag, width, most_common):
    i = width - 1
    while len(diag) > 1:
        bit = common(diag, i) ^ most_common
        diag = [n for n in diag if n >> i & 1 == bit]
        i -= 1
    return diag[0]

def oxygen(diag, width):
    return rating(diag, width, True)

def co2_scrub(diag, width):
    return rating(diag, width, False)

diag = [int(line, 2) for line in sys.stdin]
width = max(n.bit_length() for n in diag)
print(gamma(diag, width) * epsilon(diag, width))
print(oxygen(diag, width) * co2_scrub(diag, width))
