#!/usr/bin/env python3
import sys
from heapq import heappop, heappush

def parse(content):
    w = content.find('\n') + 1
    return list(map(int, content.replace('\n', '0') + w * '0')), w

def shortest_path(risk, w, source, destination):
    dist = [1 << 31] * len(risk)
    visited = [False] * len(risk)
    visited[source] = True
    prev = {}
    work = [(0, source)]

    while work:
        udist, u = heappop(work)

        if u == destination:
            total = 0
            while u != source:
                total += risk[u]
                u = prev[u]
            return total

        for nb in (u - w, u - 1, u + 1, u + w):
            if risk[nb] and not visited[nb]:
                visited[nb] = True
                alt = udist + risk[nb]
                if alt < dist[nb]:
                    dist[nb] = alt
                    prev[nb] = u
                    heappush(work, (alt, nb))

def traverse(risk, w):
    return shortest_path(risk, w, 0, len(risk) - w - 2)

def repeat(risk, w, times):
    new = []
    for y in range(times):
        for i in range(0, len(risk) - w, w):
            for x in range(times):
                new.extend((r + x + y - 1) % 9 + 1 for r in risk[i:i + w - 1])
            new.append(0)
    wnew = (w - 1) * times + 1
    new.extend([0] * wnew)
    return new, wnew

risk, w = parse(sys.stdin.read())
print(traverse(risk, w))
print(traverse(*repeat(risk, w, 5)))
