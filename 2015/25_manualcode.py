#!/usr/bin/env python3
def nth_code(n):
    code = 20151125
    for i in range(n):
        code = code * 252533 % 33554393
    return code

def code_index(row, col):
    left = col - 1
    right = row - 1
    left_bottom = col * left // 2
    right_top = row * right // 2 - right
    return row * col + left_bottom + right_top - 1

print(nth_code(code_index(3010, 3019)))
