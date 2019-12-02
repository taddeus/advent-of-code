#!/usr/bin/env python3
import sys
import re

class Reindeer:
    def __init__(self, name, speed, flight, rest):
        self.name = name
        self.speed = speed
        self.flight = flight
        self.rest = rest

    def dist(self, duration):
        elapsed = 0
        travelled = 0
        while elapsed < duration:
            elapsed += self.flight + self.rest
            travelled += self.flight * self.speed
        elapsed -= self.rest
        if elapsed > duration:
            travelled -= self.speed * (elapsed - duration)
        return travelled

    @classmethod
    def parse(cls, line):
        pat = r'(\w+) can fly (\d+) .* (\d+) .* (\d+) seconds\.'
        name, speed, flight, rest = re.match(pat, line).groups()
        return cls(name, int(speed), int(flight), int(rest))

def scores(reindeer, duration):
    for r in reindeer:
        r.period = r.flight
        r.lead = 0
        r.travelled = 0

    for sec in range(duration):
        for r in reindeer:
            if r.period > 0:
                r.travelled += r.speed
            r.period -= 1
            if r.period == -r.rest:
                r.period = r.flight

        maxdist = max(r.travelled for i, r in enumerate(reindeer))
        for r in reindeer:
            if r.travelled == maxdist:
                r.lead += 1

    return [r.lead for r in reindeer]

reindeer = list(map(Reindeer.parse, sys.stdin))
print(max(r.dist(2503) for r in reindeer))
print(max(scores(reindeer, 2503)))
