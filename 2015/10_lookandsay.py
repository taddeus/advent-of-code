#!/usr/bin/env python3
from collections import deque

def play(seq, n):
    curseq = deque(map(int, seq))
    nextseq = deque()

    for step in range(n):
        while curseq:
            i = curseq.popleft()
            count = 1
            while curseq and curseq[0] == i:
                curseq.popleft()
                count += 1
            nextseq.extend((count, i))
        curseq, nextseq = nextseq, curseq
        nextseq.clear()

    return len(curseq)

print(play('1113122113', 40))
print(play('1113122113', 50))
