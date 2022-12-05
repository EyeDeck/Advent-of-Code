import copy
import string
import sys
import re


def solve(p2):
    c = copy.deepcopy(crates)
    for m, f, t in moves:
        s = c[f - 1][-m:]
        c[t - 1].extend(s if p2 else reversed(s))
        c[f - 1] = c[f - 1][:-m]
    return ''.join([col[-1] for col in c])


day = 5
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    crates_raw, moves_raw = file.read().split('\n\n')

crate_lines = crates_raw.split('\n')
h, w = (len(crate_lines[0]) + 1) // 4, len(crate_lines)
crates = [[' ' for _ in range(w)] for _ in range(h)]
for y, line in enumerate(crates_raw.split('\n')):
    for x, char in enumerate(line):
        if char in string.ascii_letters:
            crates[x // 4][y] = char
crates = [[c for c in reversed(line) if c != ' '] for line in crates]

moves = [[int(i) for i in re.findall(r'(\d+)', line)] for line in moves_raw.split('\n') if line]

print(f'part1: {solve(False)}')
print(f'part2: {solve(True)}')
