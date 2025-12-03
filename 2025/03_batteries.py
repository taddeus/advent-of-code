#!/usr/bin/env python3
import sys

def max_joltage(bank, n):
    joltage = start = 0
    for end in range(len(bank) - n, len(bank)):
        digit = max(bank[start:end + 1])
        start = bank.index(digit, start) + 1
        joltage = joltage * 10 + digit
    return joltage

banks = [tuple(map(int, line.rstrip())) for line in sys.stdin]
print(sum(max_joltage(bank, 2) for bank in banks))
print(sum(max_joltage(bank, 12) for bank in banks))
