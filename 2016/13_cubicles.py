#!/usr/bin/env python3
from heapq import heappush, heappop

magic = 1350

def popcount(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def is_space(x, y):
    return not popcount(x*x + 3*x + 2*x*y + y + y*y + magic) % 2

def neighboring_spaces(x, y):
    if is_space(x + 1, y):
        yield x + 1, y
    if is_space(x, y + 1):
        yield x, y + 1
    if x > 0 and is_space(x - 1, y):
        yield x - 1, y
    if y > 0 and is_space(x, y - 1):
        yield x, y - 1

def uniform_cost_search(source):
    frontier = [(0, source)]
    explored = {source}
    while frontier:
        dist, u = heappop(frontier)
        yield u, dist
        for v in neighboring_spaces(*u):
            if v not in explored:
                heappush(frontier, (dist + 1, v))
                explored.add(v)

def shortest_path(source, dest):
    for node, dist in uniform_cost_search(source):
        if node == dest:
            return dist

def reachable_in(source, maxdist):
    count = 0
    for node, dist in uniform_cost_search(source):
        if dist > maxdist:
            return count
        count += 1

print(shortest_path((1, 1), (31, 39)))
print(reachable_in((1, 1), 50))
