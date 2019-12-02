#!/usr/bin/env python3
import sys
import re


def declen(data, compress_markers):
    regex = re.compile(r'\((\d+)x(\d+)\)')

    def range_len(start, end):
        m = regex.search(data, start, end)
        l = 0
        while m:
            rep_len = int(m.group(1))
            rep_times = int(m.group(2))
            l += m.start() - start
            start = m.end() + rep_len
            if compress_markers:
                rep_len = range_len(start - rep_len, start)
            l += rep_times * rep_len
            m = regex.search(data, start, end)
        l += end - start
        return l

    return range_len(0, len(data))


compressed = sys.stdin.read().rstrip()
print(declen(compressed, False))
print(declen(compressed, True))
