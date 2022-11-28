import sys
import re
import numpy as np
from collections import Counter, defaultdict  # defaultdict(int)


def p1():
    ct = 0
    for line in data:
        counted = Counter(line)
        if sum([counted[char] for char in counted if char in 'aeiou']) < 3:
            continue

        for i in range(len(line)-1):
            if line[i+1] == line[i]:
                # print(line[i], line[i+1])
                break
        else:
            continue

        if len(re.findall('(ab|cd|pq|xy)', line)) > 0:
            continue

        ct += 1
    return ct


def has_double(line):
    for i in range(len(line) - 1):
        # if len(re.findall(line[i:i + 2], line)) >= 2:
        if line.count(line[i:i + 2]) >= 2:
            print(line[i:i + 2], line)
            return True
    else:
        return False


def p2():
    ct = 0
    for line in data:
        if not has_double(line):
            continue

        for i in range(len(line)-2):
            if line[i+2] == line[i]:
                # print(line[i], line[i+1])
                break
        else:
            continue

        ct += 1


    return ct



f = 'd5.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

# print(f'part1: {p1()}')
print(f'part2: {p2()}')
