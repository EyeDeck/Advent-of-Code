import sys
import re
from math import *


def add(a, b):
    return f'[{a},{b}]'


def get_explode_index(fish):
    ct = 0
    for i, c in enumerate(fish):
        if c == ']':
            ct -= 1
        if c == '[':
            ct += 1
            if ct > 4:
                for j, c in enumerate(fish[i:]):
                    if c == ']':
                        return i, i + j
    return -1, -1


def get_bound_nums(fish, l, r):
    fishlen = len(fish)
    l2 = 0
    r2 = 0
    while l >= 0 and not fish[l].isnumeric():
        l -= 1
    l2 = l
    if l > 0:
        while fish[l2 - 1].isnumeric():
            l2 -= 1
    while r < fishlen and not fish[r].isnumeric():
        r += 1
    r2 = r
    if r < len(fish):
        while fish[r2 + 1].isnumeric():
            r2 += 1
    else:
        r, r2 = -1, -1
    return l, l2, r, r2


def try_explode(fish):
    l, r = get_explode_index(fish)
    if l == -1:
        return fish, False
    to_explode = eval(fish[l:r + 1])
    outer_l = l - 1
    outer_r = r + 1
    l1, l2, r1, r2 = get_bound_nums(fish, outer_l, outer_r)
    lhalf = fish[0:outer_l + 1]
    rhalf = fish[outer_r:]
    if l1 > 0:
        i = int(fish[l2:l1 + 1]) + to_explode[0]
        lhalf = fish[:l2] + str(i) + fish[l1 + 1:outer_l + 1]
    if r1 > 0:
        i = int(fish[r1:r2 + 1]) + to_explode[1]
        rhalf = fish[outer_r:r1] + str(i) + fish[r2 + 1:]
    out = lhalf + '0' + rhalf
    return out, True


def test_explode_once(i, o):
    print('testing', i)
    test = try_explode(i)
    assert test[0] == o
    print('passed', o, '\n')


def test_explode():
    test_explode_once('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]')
    test_explode_once('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]')
    test_explode_once('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]')
    test_explode_once('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    test_explode_once('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')
    print('tests passed')


def try_split(fish):
    m = re.search('(-?\d\d+)', fish)
    # print(m)
    if not m:
        return fish, False
    i = int(m.group(0))
    return f'{fish[:m.start()]}[{i//2},{ceil(i/2)}]{fish[m.end():]}', True


def tick_once(fish):
    fish, exploded = try_explode(fish)
    if exploded:
        return fish, True
    fish, split = try_split(fish)
    if split:
        return fish, True
    return fish, False


def reduce(fish):
    while True:
        fish, ticked = tick_once(fish)
        if not ticked:
            return fish


def r_mag(d):
    a,b = d
    if isinstance(a, list):
        a = r_mag(a)
    if isinstance(b, list):
        b = r_mag(b)
    return a*3 + b*2


def p1():
    test_explode()

    print(try_split('10'))
    print(try_split('[[[[0,7],4],[15,[0,13]]],[1,1]]'))

    print('testing file...')
    a = data[0]
    for datum in data[1:]:
        a = add(a,datum)
        a = reduce(a)
    return r_mag(eval(a))


def p2():
    mx = 0
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j:
                continue
            mx = max(mx, r_mag(eval(reduce(add(data[i],data[j])))))
    return mx


day = 18
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
