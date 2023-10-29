#!/usr/bin/env python3
import sys

def to_decimal(snafu):
    return sum(5 ** i * ('=-012'.index(digit) - 2)
               for i, digit in enumerate(reversed(snafu)))

def to_snafu(decimal):
    digits = []
    while decimal:
        decimal, rem = divmod(decimal, 5)
        decimal += rem > 2
        digits.append('012=-'[rem])
    return ''.join(reversed(digits))

print(to_snafu(sum(to_decimal(line.rstrip()) for line in sys.stdin)))
