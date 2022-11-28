import re
import sys


def any_list(dic):
    for k,v in dic.items():
        if isinstance(v,list):
            return True
    return False


def p1():
    while iterative_parse():
        pass
    if any_list(regex):
        unroll(3)
        while iterative_parse():
            pass
    print(len(regex['0']))
    ct = 0
    for s in msgs:
        founds = re.findall('^' + regex['0'] + '$', s)
        if len(founds) == 1:
            ct += 1

    return ct


def unroll(times):
    for i in range(times):
        for k,v in regex.items():
            if isinstance(v, str):
                continue
            if k in v:
                i = v.index(k)
                to_add = v.copy()
                to_add.insert(0, '(')
                to_add.append(')')
                v.pop(i)
                v[i:i] = to_add

    for k, v in regex.items():
        if isinstance(v, str):
            continue
        if k in v:
            v.pop(v.index(k))


def iterative_parse():
    def any_numbers(l):
        for i in l:
            if i.isdigit():
                return True
        return False

    worked = False
    for k, v in regex.items():
        if isinstance(v, list):
            if len(v) == 1:
                regex[k] = v[0]
                worked = True
                continue
            else:
                for i, n in enumerate(v):
                    if n.isdigit() and isinstance(regex[n], str):
                        v[i] = regex[n]
                        worked = True
            if not any_numbers(v):
                regex[k] = '(' + ''.join(v) + ')'
                worked = True
    return worked


f = 'd19.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().split('\n\n')
    rules = [line.strip() for line in data[0].split('\n')]
    msgs = [line.strip() for line in data[1].split('\n')]

regex = {}
for line in rules:
    k,v = line.strip().split(':')
    regex[k] = v.strip().strip('"').split(' ')
regex['8'] = '42 | 42 8'.split(' ')
regex['11'] = '42 31 | 42 11 31'.split(' ')

print(f'part1: {p1()}')
