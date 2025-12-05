#!/usr/bin/env python3
import sys

def remove_accessible(papers):
    for x, y in papers:
        neighbors = {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                     (x - 1, y    ),             (x + 1, y    ),
                     (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}
        if len(papers & neighbors) >= 4:
            yield x, y

def find_inaccessible(papers):
    new = set(remove_accessible(papers))
    while len(new) != len(papers):
        papers = new
        new = set(remove_accessible(papers))
    return papers

papers = {(x, y) for y, line in enumerate(sys.stdin)
                 for x, char in enumerate(line)
                 if char == '@'}
remains = set(remove_accessible(papers))
print(len(papers) - len(remains))
print(len(papers) - len(find_inaccessible(remains)))
