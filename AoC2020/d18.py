import copy
import operator
import sys


def p1():
    def evl(arr):
        if isinstance(arr, int):
            return arr
        while len(arr) >= 3:
            x, op, y = evl(arr.pop(0)), arr.pop(0), evl(arr.pop(0))
            # arr.insert(0, eval(f'{x} {op} {y}'))
            arr.insert(0, ops[op](x, y))
        return arr.pop()

    return sum([evl(line) for line in copy.deepcopy(data)])


def p2():
    def evl(arr):
        if isinstance(arr, int):
            return arr
        while len(arr) >= 3:
            if '+' in arr:
                i = arr.index('+') - 1
            else:
                i = 0
            x, op, y = evl(arr.pop(i)), arr.pop(i), evl(arr.pop(i))
            arr.insert(i, ops[op](x, y))
        return arr.pop()

    return sum([evl(line) for line in copy.deepcopy(data)])


def parse(arr):
    stack = []
    while arr:
        c = arr.pop(0)
        if c == '(':
            stack.append(parse(arr))
        elif c == ')':
            return stack
        else:
            stack.append(c)
    return stack


f = 'd18.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(i) if i.isnumeric() else i for i in line.replace(' ', '').strip()] for line in file]
    data = [parse(line) for line in data]

ops = {
    '*': lambda x, y: operator.mul(x, y),
    '+': lambda x, y: operator.add(x, y),
}

print(f'part1: {p1()}')
print(f'part2: {p2()}')
