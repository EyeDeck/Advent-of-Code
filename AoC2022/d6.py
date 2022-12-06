import sys


def solve(p2):
    l = 14 if p2 else 4
    for i in range(len(data)):
        if len(set(data[i:i+l])) == l:
            return i + l


day = 6
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().strip()

print(f'part1: {solve(False)}')
print(f'part2: {solve(True)}')
