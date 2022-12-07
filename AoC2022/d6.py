import sys


def solve(l):
    for i in range(len(data)):
        if len(set(data[i:i+l])) == l:
            return i + l


day = 6
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().strip()

print(f'part1: {solve(4)}')
print(f'part2: {solve(14)}')
