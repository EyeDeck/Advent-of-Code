import sys


def p1():
    return min([sum([abs(i-v) for v in data]) for i in range(mx)])


def p2():
    return min([sum([((d := abs(v-i))+1) * d // 2 for v in data]) for i in range(mx)])


day = 7
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [int(i) for i in file.read().split(',')]
    mx = max(data)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
