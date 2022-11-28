import sys
import re
from collections import defaultdict


def parse_line(l):
    r = re.findall(pattern, l)[0]
    return int(r[0]), int(r[1]), r[2], r[3]


def p1(lines):
    ct = 0
    for line in lines:
        min_ct, max_ct, char, password = parse_line(line)
        pw_dict = defaultdict(int)
        for c in password:
            pw_dict[c] += 1
        if min_ct <= pw_dict[char] <= max_ct:
            ct += 1
    return ct


def p2(lines):
    ct = 0
    for line in lines:
        pos1, pos2, char, password = parse_line(line)
        pass_len = len(password)

        if (pos1 <= pass_len and password[pos1-1] == char) ^ (pos2 <= pass_len and password[pos2-1] == char):
            ct += 1

    return ct


f = 'd2.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line for line in file.readlines()]
pattern = re.compile('(\d+)-(\d+) (.): (.+)')

print(f'part1: {p1(data)}')
print(f'part2: {p2(data)}')
