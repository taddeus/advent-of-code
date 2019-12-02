#!/usr/bin/env python3
import sys
def captcha(digits, offset):
    return sum(d for i, d in enumerate(digits)
               if d == digits[(i + offset) % len(digits)])
digits = list(map(int, sys.stdin.readline().rstrip()))
print(captcha(digits, 1))
print(captcha(digits, len(digits) // 2))
