#!/usr/bin/env python3
import sys
from ast import literal_eval
one = 0
two = 0
for line in sys.stdin:
    orig = line.rstrip()
    interp = literal_eval(orig)
    escaped = repr(orig.replace('"', "'")).replace("'", r'\"')
    one += len(orig) - len(interp)
    two += len(escaped) - len(orig)
print(one)
print(two)
