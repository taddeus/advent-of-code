#!/usr/bin/env python3
from heapq import heapify, heappush, heappop

def scan(depth, pad, tx, ty):
    def erode(geo_index):
        return (geo_index + depth) % 20183

    w = tx + pad + 1
    h = ty + pad + 1
    grid = [erode(x * 16807) for x in range(w)]

    for y in range(1, h):
        grid.append(erode(y * 48271))
        for x in range(1, w):
            if x == tx and y == ty:
                idx = 0
            else:
                top = grid[(y - 1) * w + x]
                left = grid[y * w + x - 1]
                idx = top * left
            grid.append(erode(idx))

    for i in range(len(grid)):
        grid[i] %= 3

    return grid, w

def shortest_path(graph, source, target):
    dist = len(graph) * [1 << 32]
    dist[source] = 0
    Q = [(dist[v], v) for v, nb in enumerate(graph) if nb]
    heapify(Q)

    while Q:
        udist, u = heappop(Q)
        if udist == dist[u]:
            if u == target:
                return udist
            for v, weight in graph[u]:
                alt = udist + weight
                if alt < dist[v]:
                    dist[v] = alt
                    heappush(Q, (alt, v))

def rescue(grid, w, tx, ty):
    # approach:
    # - build graph with (x, y, tool) tuples as vertices
    # - record weighted edges including tool switching between vertices where
    #   switching is allowed
    # - do Dijkstra on the result
    h = len(grid) // w
    def neighbours(i):
        y, x = divmod(i, w)
        if y > 0: yield i - w
        if x > 0: yield i - 1
        if x < w - 1: yield i + 1
        if y < h - 1: yield i + w

    TORCH, GEAR, NEITHER = range(3)
    tools = [
        (GEAR, TORCH),    # rocky
        (GEAR, NEITHER),  # wet
        (TORCH, NEITHER), # narrow
    ]

    # for efficiency, graph is encoded as 3 concatenated lists of (y * w + x)
    # vertices, one for each tool
    off = len(grid)
    graph = [[] for i in range(3 * off)]
    for i, sty in enumerate(grid):
        for j in neighbours(i):
            tty = grid[j]
            for stool in tools[sty]:
                for ttool in tools[tty]:
                    if ttool in tools[sty]:
                        cost = 1 if ttool == stool else 8
                        graph[i + off * stool].append((j + off * ttool, cost))

    # we start and end with a torch so in the first of 3 lists
    return shortest_path(graph, 0, ty * w + tx)

depth, tx, ty = 6084, 14, 709
grid, w = scan(depth, 15, tx, ty)
print(sum(sum(grid[y * w:y * w + tx + 1]) for y in range(ty + 1)))
print(rescue(grid, w, tx, ty))
