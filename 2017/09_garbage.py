#!/usr/bin/env python3
import sys
import re

def score(inp):
    level = score = 0
    for char in inp:
        if char == '{':
            level += 1
        elif char == '}':
            score += level
            level -= 1
    return score

inp = sys.stdin.readline().rstrip()
escaped, nescaped = re.subn(r'!.', '', inp)
stripped = re.sub(r'<[^!]*?[^>]*?>', '<>', escaped)
print(score(stripped))
print(len(inp) - len(stripped) - nescaped * 2)
