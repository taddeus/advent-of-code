#!/usr/bin/env python3
import sys

WIDTH = 5

def parse(f):
    yield list(map(int, next(f).split(',')))
    for group in f.read().split('\n\n'):
        yield list(map(int, group.split()))

def rows_cols(board):
    for i in range(0, WIDTH * WIDTH, WIDTH):
        yield set(board[i:i + WIDTH])
    for i in range(WIDTH):
        yield set(board[i::WIDTH])

def play(numbers, *boards):
    boards = [list(rows_cols(board)) for board in boards]
    for num in numbers:
        for i, board in enumerate(boards):
            for rowcol in board:
                rowcol.discard(num)
            if not all(board):
                yield sum(map(sum, board[:WIDTH])) * num
                del boards[i]

scores = play(*parse(sys.stdin))
print(next(scores))
for last in scores: pass
print(last)
