import sys
import re


def p1():
    for sue, things in data.items():
        for thing, ct in things.items():
            if p1_tgt[thing] != ct:
                break
        else:
            return sue


def p2():
    for sue, things in data.items():
        for thing, ct in things.items():
            if thing in ['cats', 'trees']:
                if ct <= p1_tgt[thing]:
                    break
            elif thing in ['pomeranians', 'goldfish']:
                if ct >= p1_tgt[thing]:
                    break
            elif p1_tgt[thing] != ct:
                break
        else:
            return sue


day = 16
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

data = {}
with open(f) as file:
    for line in file:
        s = re.sub('[:,]', '', line).split()
        d = {}
        for i in range(2, 8, 2):
            d[s[i]] = int(s[i + 1])
        data[int(s[1])] = d

p1_tgt = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}

print(f'part1: {p1()}')
print(f'part2: {p2()}')
