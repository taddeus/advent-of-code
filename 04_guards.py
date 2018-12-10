#!/usr/bin/env python3
import sys
import re

patterns = {}
for line in sorted(sys.stdin):
    minute, cmd, arg = re.search(r':(\d+)] (\w+) #?(\w+)', line).groups()
    if cmd == 'Guard':
        guard = int(arg)
    elif cmd == 'falls':
        start = int(minute)
    else:
        pat = patterns.setdefault(guard, [0] * 60)
        for i in range(start, int(minute)):
            pat[i] += 1

def strategy(i, key):
    guard, pat = max(patterns.items(), key=lambda x: key(x[1]))
    bestmin = max(enumerate(pat), key=lambda x: x[1])[0]
    print('strategy %d:' % i, guard, '*', bestmin, '=', guard * bestmin)

strategy(1, sum)
strategy(2, max)
