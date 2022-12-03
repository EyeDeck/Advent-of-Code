import string
import sys

day = 3
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

priorities = {v: k + 1 for k, v in enumerate(string.ascii_lowercase + string.ascii_uppercase)}

print(f'part1: {sum(priorities[set(line[:len(line) // 2]).intersection(line[len(line) // 2:]).pop()] for line in data)}')
print(f'part2: {sum(priorities[set.intersection(*[set(g) for g in data[i:i + 3]]).pop()] for i in range(0, len(data), 3))}')
