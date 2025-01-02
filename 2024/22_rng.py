#!/usr/bin/env python3
import sys
from itertools import chain, islice, pairwise

def permute(num):
    num = (num ^ num << 6) & 0xffffff
    num ^= num >> 5
    return (num ^ num << 11) & 0xffffff

def prices(num):
    while True:
        yield num % 10
        num = permute(num)

def window(seq, n):
    win = tuple(islice(seq, n))
    yield win
    for elem in seq:
        win = win[1:] + (elem,)
        yield win

def sequence_prices(num):
    seen = {}
    for nums in window(islice(prices(num), 2001), 5):
        diffs = tuple(b - a for a, b in pairwise(nums))
        seen.setdefault(diffs, nums[-1])
    return seen

def max_prices(initials):
    combined = {}
    for num in initials:
        for diffs, price in sequence_prices(num).items():
            combined[diffs] = combined.get(diffs, 0) + price
    return max(combined.values())

def nth(num, n):
    for _ in range(n):
        num = permute(num)
    return num

initials = list(map(int, sys.stdin))
print(sum(nth(num, 2000) for num in initials))
print(max_prices(initials))
