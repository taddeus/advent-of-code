#!/usr/bin/env python3
import sys
import re

def mul(program):
    return sum(int(m[1]) * int(m[2]) for m in
               re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', program))

program = sys.stdin.read()
print(mul(program))
print(mul(re.sub(r'don\'t\(\).*?(do\(\)|$)', '', program, flags=re.DOTALL)))
