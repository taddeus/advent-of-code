#!/usr/bin/env python3
import sys
from operator import mul, floordiv, add, sub

class Expr:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return '(%s %s %s)' % (self.left, self.op, self.right)

def simplify(expr, solve=None):
    if isinstance(expr, (int, str)):
        return expr
    left = simplify(expr.left)
    right = simplify(expr.right)
    if isinstance(left, int) and isinstance(right, int):
        fn = {'*': mul, '/': floordiv, '-': sub, '+': add}[expr.op]
        return fn(left, right)
    if isinstance(left, int) and expr.op in '*+':
        return simplify(Expr(right, expr.op, left))
    if expr.op == '=' and isinstance(left, Expr):
        if isinstance(left.right, int):
            inv = {'*': '/', '/': '*', '-': '+', '+': '-'}[left.op]
            return simplify(Expr(left.left, '=', Expr(right, inv, left.right)))
        if isinstance(left.left, int) and left.op == '-':
            return simplify(Expr(left.right, '=', Expr(left.left, '-', right)))
    if expr.op == '=' and left == solve:
        return right
    return Expr(left, expr.op, right)

def parse(tasks, monkey):
    task = tasks[monkey]
    if ' ' in task:
        left, op, right = task.split()
        return Expr(parse(tasks, left), op, parse(tasks, right))
    return int(task) if task.isdigit() else task

tasks = dict(line.rstrip().split(': ') for line in sys.stdin)
print(simplify(parse(tasks, 'root')))
tasks['humn'] = 'humn'
left, _, right = tasks['root'].split()
tasks['root'] = left + ' = ' + right
print(simplify(parse(tasks, 'root')))
