#!/usr/bin/env python3
import sys

def parse(f):
    walls = set()
    boxes = {}
    for y, line in enumerate(f):
        if line == '\n':
            break
        for x, cell in enumerate(line):
            if cell == '#':
                walls.add((x, y))
            elif cell == 'O':
                boxes[x, y] = (x, y),
            elif cell == '@':
                yield x, y
    yield walls
    yield boxes
    yield [((0, -1), (0, 1), (-1, 0), (1, 0))['^v<>'.index(c)]
           for line in f for c in line if c != '\n']

def push(robot, walls, boxes, moves):
    for dx, dy in moves:
        move = lambda xy: (xy[0] + dx, xy[1] + dy)
        nb = move(robot)
        if nb not in walls:
            pushed = set()
            work = [nb]
            while work:
                xy = work.pop()
                box = boxes.get(xy, None)
                if box and box not in pushed:
                    pushed.add(box)
                    for xy in box:
                        work.append(move(xy))

            if all(move(xy) not in walls for box in pushed for xy in box):
                for box in pushed:
                    for xy in box:
                        del boxes[xy]
                for box in pushed:
                    newbox = tuple(move(xy) for xy in box)
                    for xy in newbox:
                        boxes[xy] = newbox
                robot = nb

    return sum(100 * y + x for box in set(boxes.values()) for x, y in box[:1])

def widen(robot, walls, boxes):
    x, y = robot
    yield x * 2, y
    yield {(x * 2, y) for x, y in walls} | {(x * 2 + 1, y) for x, y in walls}
    newboxes = {}
    for x, y in boxes:
        l = x * 2, y
        r = x * 2 + 1, y
        newboxes[l] = newboxes[r] = l, r
    yield newboxes

robot, walls, boxes, moves = parse(sys.stdin)
print(push(robot, walls, boxes, moves))
print(push(*widen(robot, walls, boxes), moves))
