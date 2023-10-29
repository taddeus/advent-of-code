#!/usr/bin/env python3
import sys

def parse(inp):
    chartlines, pathline = inp.read().split('\n\n')
    chart = chartlines.split('\n')
    width = max(map(len, chart)) + 2
    chart = [' ' + line + ' ' * (width - len(line) - 1) for line in chart]
    chart = [' ' * width, *chart, ' ' * width]

    path = ''
    buf = ''
    for char in pathline:
        if char.isdigit():
            buf += char
        else:
            path += 'F' * int(buf)
            buf = ''
            if char in 'LR':
                path += char

    return chart, path

def walk(chart, path, teleports={}):
    w = len(chart[0])
    h = len(chart)
    x, y = chart[1].index('.'), 1
    face = 0
    for step in path:
        if step == 'F':
            dx, dy = ((1, 0), (0, 1), (-1, 0), (0, -1))[face]
            newx = x + dx
            newy = y + dy
            newface = face
            if (newx, newy, face) in teleports:
                newx, newy, newface = teleports[(newx, newy, face)]
            while chart[newy][newx] == ' ':
                newx = (newx + dx) % w
                newy = (newy + dy) % h
            if chart[newy][newx] == '.':
                x = newx
                y = newy
                face = newface
        elif step == 'L':
            face = (face + 3) % 4
        elif step == 'R':
            face = (face + 1) % 4
    return 1000 * y + 4 * x + face

RIGHT, DOWN, LEFT, UP = range(4)
cube_sides = {}
for y1, y2 in zip(range(1, 51), range(150, 100, -1)):
    cube_sides[(50, y1, LEFT)] = 1, y2, RIGHT
    cube_sides[(0, y2, LEFT)] = 51, y1, RIGHT
    cube_sides[(151, y1, RIGHT)] = 100, y2, LEFT
    cube_sides[(101, y2, RIGHT)] = 150, y1, LEFT
for y1, x2 in zip(range(51, 101), range(1, 51)):
    cube_sides[(50, y1, LEFT)] = x2, 101, DOWN
    cube_sides[(x2, 100, UP)] = 51, y1, RIGHT
for x1, y2 in zip(range(51, 101), range(151, 201)):
    cube_sides[(x1, 0, UP)] = 1, y2, RIGHT
    cube_sides[(0, y2, LEFT)] = x1, 1, DOWN
for x1, x2 in zip(range(101, 151), range(1, 51)):
    cube_sides[(x1, 0, UP)] = x2, 200, UP
    cube_sides[(x2, 201, DOWN)] = x1, 1, DOWN
for y1, x2 in zip(range(51, 101), range(101, 151)):
    cube_sides[(101, y1, RIGHT)] = x2, 50, UP
    cube_sides[(x2, 51, DOWN)] = 100, y1, LEFT
for y1, x2 in zip(range(151, 201), range(51, 101)):
    cube_sides[(51, y1, RIGHT)] = x2, 150, UP
    cube_sides[(x2, 151, DOWN)] = 50, y1, LEFT

chart, path = parse(sys.stdin)
print(walk(chart, path))
print(walk(chart, path, cube_sides))
