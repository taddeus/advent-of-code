#!/usr/bin/env python3
import sys

def read_dots(f):
    for line in f:
        if line == '\n':
            break
        x, y = line.split(',')
        yield int(x), int(y)

def read_folds(f):
    for line in f:
        axis, at = line.split()[-1].split('=')
        yield axis == 'y', int(at)

def flip(i, at):
    return i if i < at else i - 2 * (i - at)

def fold(dots, up, at):
    return {(x, flip(y, at)) if up else (flip(x, at), y) for x, y in dots}

def plot(dots):
    xmin = min(x for x, y in dots)
    xmax = max(x for x, y in dots)
    ymin = min(y for x, y in dots)
    ymax = max(y for x, y in dots)
    for y in range(ymin, ymax + 1):
        print(''.join(' #'[(x, y) in dots] for x in range(xmin, xmax + 1)))

dots = list(read_dots(sys.stdin))
first_fold, *other_folds = read_folds(sys.stdin)
dots = fold(dots, *first_fold)
print(len(dots))

for up, at in other_folds:
    dots = fold(dots, up, at)
plot(dots)
