#!/usr/bin/env python3
import sys
from collections import deque

def parse(nums):
    nchildren = nums.popleft()
    nmeta = nums.popleft()
    children = [parse(nums) for i in range(nchildren)]
    meta = [nums.popleft() for i in range(nmeta)]
    return children, meta

def addmeta(node):
    children, meta = node
    return sum(meta) + sum(map(addmeta, children))

def value(node):
    c, m = node
    return sum(value(c[i - 1]) for i in m if 1 <= i <= len(c)) if c else sum(m)

root = parse(deque(map(int, sys.stdin.read().split())))
print(addmeta(root))
print(value(root))
