#!/usr/bin/env python3
import sys
from collections import deque

reqs = {}
for line in sys.stdin:
    a, b = line[5:37:31]
    reqs.setdefault(b, set()).add(a)
    reqs.setdefault(a, set())

# part 1
worklist = deque()
remain = set(reqs)
while remain:
    nxt = min(k for k in remain if not reqs[k] & remain)
    remain.remove(nxt)
    worklist.append(nxt)

print(''.join(worklist))

# part 2
working = []
completed = set()
tick = -1

while worklist:
    tick += 1
    completed |= set(task for task, rem in working if rem == 1)
    working = [(task, rem - 1) for task, rem in working if rem > 1]

    while len(working) < 5:
        for task in worklist:
            if not reqs[task] - completed:
                worklist.remove(task)
                working.append((task, ord(task) - 4))
                break
        else:
            break

print(tick + max(rem for task, rem in working))
