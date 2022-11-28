import re
import sys


def p1():
    while iterative_parse():
        #print(regex)
        #input()
        pass
    ct = 0
    for s in msgs:
        founds = re.findall('^' + regex['0'] + '$', s)
        if len(founds) == 1:
            ct += 1

    return ct


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

print(f'part1: {p1()}')
