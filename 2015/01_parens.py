#!/usr/bin/env python3
import sys
line = sys.stdin.readline().rstrip()
print(line.count('(') - line.count(')'))
total = 0
for index, c in enumerate(line):
    total += 1 if c == '(' else -1
    if total == -1:
        break
print(index + 1)
