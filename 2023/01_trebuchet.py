#!/usr/bin/env python3
import sys
import re

WORDS = r'\d one two three four five six seven eight nine'.split()

def digit(d):
    return int(d) if d.isdigit() else WORDS.index(d)

def calibrate(line, pattern):
    first = re.search(pattern, line)
    last = re.match('.*(%s)' % pattern, line[first.end():])
    return digit(first[0]) * 10 + digit(last[1] if last else first[0])

lines = sys.stdin.readlines()
print(sum(calibrate(line, r'\d') for line in lines))
print(sum(calibrate(line, '|'.join(WORDS)) for line in lines))
