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
    all_seq_prices = list(map(sequence_prices, initials))
    sequences = set(chain.from_iterable(all_seq_prices))
    return max(sum(seq_prices.get(seq, 0) for seq_prices in all_seq_prices)
               for seq in sequences)

def nth(num, n):
    for _ in range(n):
        num = permute(num)
    return num

initials = list(map(int, sys.stdin))
print(sum(nth(num, 2000) for num in initials))
print(max_prices(initials))
