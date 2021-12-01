#!/usr/bin/env python3
import sys

def slide(depths, winsize):
    return [sum(depths[i:i + winsize])
            for i in range(len(depths) - winsize + 1)]

def increased(depths):
    return sum(depths[i] < depths[i + 1] for i in range(len(depths) - 1))

depths = list(map(int, sys.stdin))
print(increased(slide(depths, 1)))
print(increased(slide(depths, 3)))
