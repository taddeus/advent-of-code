#!/usr/bin/env python3
import sys

def parse(line):
    nums, char, pw = line.rstrip().split()
    lo, hi = nums.split('-')
    return int(lo), int(hi), char[0], pw

def valid1(lo, hi, char, pw):
    return lo <= pw.count(char) <= hi

def valid2(lo, hi, char, pw):
    return lo == hi or (pw[lo - 1] + pw[hi - 1]).count(char) == 1

passwords = list(map(parse, sys.stdin))
print(sum(valid1(*p) for p in passwords))
print(sum(valid2(*p) for p in passwords))
