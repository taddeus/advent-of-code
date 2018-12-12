#!/usr/bin/env python3
import sys

initial = sys.stdin.readline().split()[-1].replace('.', ' ')
sys.stdin.readline()
trans = dict(tuple(line.rstrip().replace('.', ' ').split(' => '))
             for line in sys.stdin)

def spread(iters):
    offset = 0
    pattern = initial
    for i in range(iters):
        pattern = '    ' + pattern + '    '
        leftpad = ''.join(trans.get(pattern[i - 2: i + 3], ' ')
                          for i in range(2, len(pattern) - 2)).rstrip()
        stripped = leftpad.lstrip()
        offset += len(leftpad) - len(stripped) - 2
        pattern = stripped
    return sum(i + offset for i, c in enumerate(pattern) if c == '#')

print(spread(20))
n = 500
a = spread(n)
b = spread(n + 1)
print(a + (b - a) * (50000000000 - n))
