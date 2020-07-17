#!/usr/bin/env python3
from collections import namedtuple
from queue import PriorityQueue

State = namedtuple('State', 'floors elevator')

def get_score(state):
    # - lower accumulated distance of all elements to floor 4 = better
    # - elevator position closer to lowest item = better
    accumulated_distance = 0
    elevator_to_bottom = None
    top_dist = len(state.floors) - 1
    for i, (rtgs, chips) in enumerate(state.floors):
        nitems = len(rtgs) + len(chips)
        accumulated_distance += top_dist * nitems
        top_dist -= 1
        if nitems > 0 and elevator_to_bottom is None:
            elevator_to_bottom = state.elevator - i
    return accumulated_distance, elevator_to_bottom

def is_valid(state):
    def floor_valid(rtgs, chips):
        return len(rtgs) == 0 or all(ty in rtgs for ty in chips)
    return 0 <= state.elevator < len(state.floors) and \
           all(floor_valid(r, c) for r, c in state.floors)

def add_to_floor(floor, new_rtgs, new_chips):
    old_rtgs, old_chips = floor
    return old_rtgs + new_rtgs, old_chips + new_chips

def valid_steps(state):
    floors, el = state

    def select(s):
        if len(s) > 0:
            for i, c in enumerate(s):
                yield c, s[:i] + s[i + 1:]

    def move_up(rtg, rem_rtgs, chip, rem_chips):
        cur = rem_rtgs, rem_chips
        top = add_to_floor(floors[el + 1], rtg, chip)
        return State(floors[:el] + (cur, top) + floors[el + 2:], el + 1)

    def move_down(rtg, rem_rtgs, chip, rem_chips):
        cur = rem_rtgs, rem_chips
        bot = add_to_floor(floors[el - 1], rtg, chip)
        return State(floors[:el - 1] + (bot, cur) + floors[el + 1:], el - 1)

    def gen_steps():
        rtgs, chips = floors[el]
        for rtg1, rem_rtgs1 in select(rtgs):
            if el < len(floors) - 1:
                for rtg2, rem_rtgs2 in select(rem_rtgs1):
                    yield move_up(rtg1 + rtg2, rem_rtgs2, '', chips)
                for chip, rem_chips in select(chips):
                    yield move_up(rtg1, rem_rtgs1, chip, rem_chips)
                yield move_up(rtg1, rem_rtgs1, '', chips)
            if el > 0:
                yield move_down(rtg1, rem_rtgs1, '', chips)
        for chip1, rem_chips1 in select(chips):
            if el < len(floors) - 1:
                for chip2, rem_chips2 in select(rem_chips1):
                    yield move_up('', rtgs, chip1 + chip2, rem_chips2)
                yield move_up('', rtgs, chip1, rem_chips1)
            if el > 0:
                yield move_down('', rtgs, chip1, rem_chips1)

    return filter(is_valid, gen_steps())

def min_steps(initial):
    worklist = PriorityQueue()
    seen = {initial}
    worklist.put((get_score(initial), 0, initial))
    while not worklist.empty():
        score, steps, state = worklist.get()
        if score == (0, 0):
            return steps
        for next_state in valid_steps(state):
            if next_state not in seen:
                worklist.put((get_score(next_state), steps + 1, next_state))
                seen.add(next_state)

assert min_steps(State((('', 'HL'), ('H', ''), ('L', ''), ('', '')), 0)) == 11

part1 = min_steps(State((('SP', 'SP'), ('TRC', 'RC'), ('', 'T'), ('', '')), 0))
print(part1)
print(part1 + min_steps(State((('ED', 'ED'), ('', ''), ('', ''), ('S', 'S')), 3)))
#print(min_steps(State((('SPED', 'SPED'), ('TRC', 'RC'), ('', 'T'), ('', '')), 0)))
