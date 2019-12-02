#!/usr/bin/env python3
import sys
import json
import re
from pprint import pprint

def jsum(data, ignore=None):
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        return sum(jsum(v, ignore) for v in data)
    if isinstance(data, dict) and ignore not in data.values():
        return sum(jsum(v, ignore) for v in data.values())
    return 0

data = json.load(sys.stdin)
print(jsum(data))
print(jsum(data, 'red'))
