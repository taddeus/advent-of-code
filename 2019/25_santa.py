#!/usr/bin/env python3
import re
import sys
from itertools import combinations
from intcode import read_program, run

def send_command(droid, command):
    inputs = map(ord, command + '\n') if command else []
    buf = [chr(outp) for outp in map(droid.send, inputs) if outp is not None]
    for outp in droid:
        if outp is None:
            break
        buf.append(chr(outp))
    return ''.join(buf)

def parse_output(output):
    assert output.endswith('Command?\n')
    loc = re.search(r'== (.*) ==', output, re.M).group(1)
    directions = re.findall(r'- (north|south|east|west)', output)
    m = re.search(r'Items here:', output)
    items = re.findall(r'- (.*)', output[m.end(0):]) if m else []
    return loc, directions, items

def play(droid):
    opposite_directions = {'north': 'south', 'south': 'north',
                           'west': 'east', 'east': 'west', '': ''}
    dangerous_items = {'escape pod', 'giant electromagnet', 'photons',
                       'molten lava', 'infinite loop'}

    def dfs(prev, direction, path):
        nonlocal destination_path
        output = send_command(droid, direction)
        loc, directions, items = parse_output(output)
        for item in items:
            if item not in dangerous_items:
                send_command(droid, 'take ' + item)
                inventory.append(item)
        if loc == 'Pressure-Sensitive Floor':
            destination_path = tuple(path)
        if loc not in visited:
            visited.add(loc)
            for d in directions:
                if d != opposite_directions[direction]:
                    dfs(loc, d, path + [d])
                    send_command(droid, opposite_directions[d])

    inventory = []
    destination_path = None
    visited = {'outside'}
    dfs('outside', '', [])

    for direction in destination_path[:-1]:
        send_command(droid, direction)

    for dropnum in range(len(inventory)):
        for dropitems in combinations(inventory, dropnum):
            for item in dropitems:
                send_command(droid, 'drop ' + item)
            output = send_command(droid, destination_path[-1])
            if 'Alert!' not in output:
                return int(re.search(r'\d+', output).group(0))
            for item in dropitems:
                send_command(droid, 'take ' + item)

print(play(run(read_program(sys.stdin))))
