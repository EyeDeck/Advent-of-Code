import copy
import operator
import sys


def solve(monkeys):
    while isinstance(monkeys['root'], list):
        for monkey_name, monkey_data in monkeys.items():
            if isinstance(monkey_data, list):
                l, op, r = monkey_data
                if isinstance(monkeys[l], int) and isinstance(monkeys[r], int):
                    l, r = monkeys[l], monkeys[r]
                    monkeys[monkey_name] = op(l, r)
                    # if monkey_name == 'root':
                    #     print(l, r, l > r, monkeys['root'])
    return monkeys['root']


def p2():
    # work out the correct uppermost bit
    place = 1
    data['root'][1] = operator.ge
    data['humn'] = place
    while solve(copy.deepcopy(data)):
        place += 1
        data['humn'] = 1 << place
    n = 1 << (place-1)

    # now binary search the lower bits
    data['root'][1] = operator.lt
    for i in range(place, -1, -1):
        if i == 0:
            data['root'][1] = operator.eq

        data['humn'] = n + (1 << i)
        if not solve(copy.deepcopy(data)):
            n += (1 << i)
    return n


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

print('part1:', solve(copy.deepcopy(data)))
print('part2:', p2())
