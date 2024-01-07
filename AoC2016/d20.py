from aoc import *


def solve():
    cleaned = []
    stack = deque(data)
    while len(stack) > 1:
        a, b = stack.popleft(), stack.popleft()
        # print(a, b)
        if a[1] >= b[0]-1:
            stack.appendleft((min(a[0],b[0]),max(a[1],b[1])))
        else:
            cleaned.append(a)
            stack.appendleft(b)

    cleaned.append(stack.pop())

    return cleaned[0][1]+1, 4294967296 - sum(b-a+1 for a,b in cleaned)


setday(20)

data = [tuple(int(n) for n in line.split('-')) for line in parselines()]
data.sort()

print('part1: %s\npart2: %s' % solve())