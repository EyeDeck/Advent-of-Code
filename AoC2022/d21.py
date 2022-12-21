import copy
import operator
import sys


def p1():
    monkeys = copy.deepcopy(data)
    while not isinstance(monkeys['root'], int):
        for name, d in monkeys.items():
            if isinstance(d, int):
                pass
            else:
                l, op, r = d
                # print(l, op, r)
                if isinstance(monkeys[l], int) and isinstance(monkeys[r], int):
                    # print(l, r)
                    l, r = monkeys[l], monkeys[r]
                    monkeys[name] = op(l, r)
    return monkeys['root']


def p2():
    next_i = 1
    while True:
        # print(next_i, end='\r')
        monkeys = copy.deepcopy(data)
        monkeys['root'][1] = operator.eq
        monkeys['humn'] = next_i
        while not isinstance(monkeys['root'], int):
            for name, d in monkeys.items():
                if isinstance(d, int):
                    pass
                else:
                    l, op, r = d
                    # print(l, op, r)
                    if isinstance(monkeys[l], int) and isinstance(monkeys[r], int):
                        # print(l, r)
                        l, r = monkeys[l], monkeys[r]
                        monkeys[name] = op(l, r)

                        if monkeys['root'] == True:
                            return next_i

                        if name == 'root':
                            print(l, r, l>r) # , end='\r')
                            # next_i = l // 2
                            next_i = int(input('next? '))



day = 21
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv
}

data = {}

with open(f) as file:
    for line in file:
        parts = line.strip().split(' ')
        name = parts[0][:-1]
        if len(parts) == 2:
            data[name] = int(parts[1])
        else:
            data[name] = [parts[1], operators[parts[2]], parts[3]]

print('part1:', p1() )
print('part2:', p2() )
