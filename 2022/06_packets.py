#!/usr/bin/env python3
import sys
from collections import deque

def marker(stream, winlen):
    window = deque(stream[:winlen - 1])
    for i, char in enumerate(stream[winlen - 1:]):
        if char not in window and len(set(window)) == winlen - 1:
            return i + winlen
        window.popleft()
        window.append(char)

stream = sys.stdin.readline().rstrip()
print(marker(stream, 4))
print(marker(stream, 14))
