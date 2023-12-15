#!/usr/bin/env python3
import sys

def asciihash(s):
    h = 0
    for char in s:
        h = (h + ord(char)) * 17 % 256
    return h

def focus(steps):
    boxes = [({}, []) for _ in range(256)]

    for step in steps:
        if step.endswith('-'):
            label = step[:-1]
            index, powers = boxes[asciihash(label)]
            if label in index:
                powers[index.pop(label)] = None
        else:
            label, power = step.split('=')
            index, powers = boxes[asciihash(label)]
            if label in index:
                powers[index[label]] = int(power)
            else:
                index[label] = len(powers)
                powers.append(int(power))

    return sum(sum((b + 1) * (i + 1) * power
                   for i, power in enumerate(filter(None, powers)))
               for b, (_, powers) in enumerate(boxes))

steps = next(sys.stdin).rstrip().split(',')
print(sum(map(asciihash, steps)))
print(focus(steps))
