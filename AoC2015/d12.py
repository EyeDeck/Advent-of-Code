import sys
import re
import json


def p1():
    return sum([int(i) for i in re.findall('-?\d+', data)])


def rsum(obj):
    total = 0
    # print(obj)
    if isinstance(obj, str):
        return 0
    elif isinstance(obj, int):
        return obj
    elif isinstance(obj, tuple) or isinstance(obj, list):
        for thing in obj:
            total += rsum(thing)
    elif isinstance(obj, dict):
        if 'red' in obj.values():
            return 0
        for thing in obj.items():
            total += rsum(thing)
    return total


def p2():
    return rsum(json.loads(data))


day = 12
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().strip()

print(f'part1: {p1()}')
print(f'part2: {p2()}')
