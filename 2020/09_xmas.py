#!/usr/bin/env python3
import sys
from collections import deque

def find_invalid(seq, winsize):
    win = seq[:winsize]
    valid = deque([a + b for b in win if a != b] for a in win)

    for i, num in enumerate(seq[winsize:]):
        if not any(num in v for v in valid):
            return num
        valid.popleft()
        valid.append([num + b for b in seq[i:i + winsize]])

def weakness(seq, invalid):
    win = deque()
    total = 0
    for num in seq:
        while total > invalid:
            total -= win.popleft()
        if total == invalid:
            return min(win) + max(win)
        win.append(num)
        total += num

seq = list(map(int, sys.stdin))
invalid = find_invalid(seq, 25)
print(invalid)
print(weakness(seq, invalid))
