from aoc import *


def p1():
    s = 0
    ind = string.ascii_lowercase + string.ascii_uppercase
    print(ind)
    for line in data:
        l, r = line[:len(line)//2], line[len(line)//2:]
        l = set(l)
        r = set(r)
        i = r.intersection(l)
        s += ind.find(i.pop()) + 1
    return s


def p2():
    s = 0
    ind = string.ascii_lowercase + string.ascii_uppercase
    print(ind)
    for i in range(0, len(data), 3):
        xyz = [set(l) for l in data[i:i+3]]
        # print(xyz)
        # print(xyz[0].intersection(xyz[1]))
        s += ind.find( xyz[0].intersection(xyz[1]).intersection(xyz[2]).pop() ) + 1
        continue
        # l, r = line[:len(line) // 2], line[len(line) // 2:]
        # l = set(l)
        # r = set(r)
        # i = r.intersection(l)
        # s += ind.find(i.pop()) + 1
    return s


day = 3
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

# with open(f) as file:
#     data = [line.strip() for line in file]
data = heurparse(f)


print(f'part1: {p1()}')
print(f'part2: {p2()}')
