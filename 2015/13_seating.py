#!/usr/bin/env python3
import sys
import re
from collections import defaultdict
from itertools import permutations

graph = defaultdict(lambda: defaultdict(int))
pat = re.compile(r'(\w+) would (gain|lose) (\d+) .* to (\w+)\.')
for line in sys.stdin:
    a, sign, diff, b = pat.match(line).groups()
    diff = int(diff) * (-1 if sign == 'lose' else 1)
    graph[a][b] += diff
    graph[b][a] += diff

def score(people):
    score = graph[people[0]][people[-1]]
    for i in range(len(people) - 1):
        score += graph[people[i]][people[i + 1]]
    return score

def bestscore(people):
    return max(map(score, permutations(people)))

everyone = list(graph.keys())
print(bestscore(everyone))
print(bestscore(everyone + ['me']))
