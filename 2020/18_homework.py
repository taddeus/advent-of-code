#!/usr/bin/env python3
import re
import sys

class Term(int):
    def __mul__(self, other): return Term(int.__mul__(self, other))
    def __add__(self, other): return Term(int.__add__(self, other))
    __sub__ = __mul__
    __pow__ = __add__

exprs = re.sub(r'(\d+)', r'Term(\1)', sys.stdin.read()).splitlines()
print(sum(eval(e.replace('*', '-')) for e in exprs))
print(sum(eval(e.replace('+', '**')) for e in exprs))
