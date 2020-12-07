#!/usr/bin/env python3
import re
import sys

def parse(f):
    contains = {}
    contained_by = {}
    for line in f:
        parent, children = line.split(' bags contain ')
        contains[parent] = parent_contains = {}
        for match in re.findall(r'\d+ \w+ \w+', children):
            num, child = match.split(' ', 1)
            parent_contains[child] = int(num)
            contained_by.setdefault(child, []).append(parent)
    return contains, contained_by

def containers(color, contained_by):
    def traverse(child):
        for parent in contained_by.get(child, []):
            yield parent
            yield from traverse(parent)
    return set(traverse(color))

def count(color, contains):
    return sum(n + n * count(c, contains) for c, n in contains[color].items())

contains, contained_by = parse(sys.stdin)
print(len(containers('shiny gold', contained_by)))
print(count('shiny gold', contains))
