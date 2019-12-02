#!/usr/bin/env python3
import sys

def parse(f):
    for line in f:
        depth, ran = map(int, line.split(': '))
        yield depth, ran

def period(ran):
    return 2 * (ran - 1)

def severity(ranges):
    return sum(depth * ran for depth, ran in ranges if depth % period(ran) == 0)

def caught(ranges, delay):
    return any((depth + delay) % period(ran) == 0 for depth, ran in ranges)

def find_delay(ranges):
    delay = 0
    while caught(ranges, delay):
        delay += 1
    return delay

ranges = list(parse(sys.stdin))
print(severity(ranges))
print(find_delay(ranges))
