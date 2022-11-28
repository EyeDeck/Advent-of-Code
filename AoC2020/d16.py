import sys
import re
from collections import *


def p1():
    return sum(sum([x for x in [valid_for_any_field(n) for n in ticket] if x is not None]) for ticket in tickets)


def valid_for_any_field(n):
    for field in fields:
        if (field[0] <= n <= field[1]) or (field[2] <= n <= field[3]):
            break
    else:
        return n
    return None


def is_ticket_valid(ticket):
    for i, n in enumerate(ticket):
        if valid_for_any_field(n) is not None:
            return False
    return True


def is_valid_for_field(col, field):
    for n in col:
        if (field[0] <= n <= field[1]) or (field[2] <= n <= field[3]):
            pass
        else:
            return False
    return True


def p2():
    valids = [x for x in tickets if is_ticket_valid(x)]

    cols = [[] for _ in range(len(valids[0]))]

    for row in range(len(valids)):
        for column in range(len(valids[0])):
            cols[column].append(valids[row][column])

    possible = defaultdict(set)
    for i, col in enumerate(cols):
        for j, field in enumerate(fields):
            if is_valid_for_field(col, field):
                possible[i].add(j)

    definite = [0 for _ in range(len(possible))]
    while len(possible):
        found_col = min(possible, key=lambda key: len(possible[key]))
        col = possible[found_col].pop()
        possible.pop(found_col)
        definite[col] = found_col

        for k in possible.keys():
            possible[k].discard(col)

    n = 1
    for i in range(6):
        n *= my_ticket[definite[i]]
    print(definite)

    return n


f = 'd16.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file.read().split('\n\n')]

fields = [tuple(int(i) for i in re.findall('(\\d+)', line)) for line in data[0].split('\n')]
my_ticket = [int(i.strip()) for i in data[1].split('\n')[1].split(',')]
tickets = [[int(i.strip()) for i in line.split(',')] for line in data[2].split('\n')[1:]]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
