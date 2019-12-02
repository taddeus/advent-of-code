#!/usr/bin/env python3
import sys

def escape(maze, decrease):
    vis = [0] * len(maze)
    steps = 0
    pos = 0
    while 0 <= pos < len(maze):
        jump = maze[pos] + vis[pos]
        vis[pos] += -1 if decrease and jump >= 3 else 1
        pos += jump
        steps += 1
    return steps

maze = list(map(int, sys.stdin))
print(escape(maze, False))
print(escape(maze, True))
