#!/usr/bin/env python3
import sys

def fft(seq):
    end = len(seq)
    windows = [(i, 1, i + 1, seq[i]) for i in range(0, end, 2)]
    for i in range(end):
        newval = 0
        multiplier = 1
        newwins = []
        for start, size, shift, winsum in windows:
            newval = newval + winsum * multiplier
            multiplier *= -1
            if start + shift < end:
                winsum -= sum_at(seq, start, shift)
                winsum += sum_at(seq, start + size, shift + 1)
                newwins.append((start + shift, size + 1, shift, winsum))
        seq[i] = abs(newval) % 10
        windows = newwins

def join(seq):
    return ''.join(map(str, seq))

def message(seq, offset):
    seq = list(seq)
    for i in range(100):
        fft(seq)
    return join(seq[offset:offset + 8])

def sum_at(seq, start, size):
    return sum(seq[start:start + size])

def fft_at(seq, start):
    assert start > len(seq) // 2
    size = start + 1
    winsum = sum_at(seq, start, size)

    for i in range(start, len(seq)):
        newdigit = abs(winsum) % 10
        winsum += sum_at(seq, start + size, 2) - seq[start]
        start += 1
        size += 1
        seq[i] = newdigit

def message_at(seq, start):
    for i in range(100):
        fft_at(seq, start)
    return join(seq[start:start + 8])

seq = list(map(int, sys.stdin.readline().rstrip()))
print(message(seq, 0))
print(message_at(seq * 10000, int(join(seq[:7]))))
