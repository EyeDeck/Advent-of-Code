import sys


def p1(d):
    return sum([len(set(x.replace(' ', ''))) for x in d])


def p2(d):
    ct = 0
    for line in d:
        qs = line.split(' ')
        running = set(qs[0])
        for q in qs[1:]:
            running = running.intersection(q)
        ct += len(running)
    return ct


f = 'd6.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.replace('\n', ' ') for line in file.read().split('\n\n')]

print(f'part1: {p1(data)}')
print(f'part2: {p2(data)}')
