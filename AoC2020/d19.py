import sys
import re

f = 'd19.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().split('\n\n')
    print(data)
    rules = [line.strip() for line in data[0].split('\n')]
    msgs = [line.strip() for line in data[1].split('\n')]

regex = {}
for line in rules:
    k,v = line.strip().split(':')
    regex[k] = v.strip().strip('"').split(' ')

print(regex)


def any_numbers(l):
    for i in l:
        if i.isdigit():
            return True
    return False


def iterative_parse(rx):
    worked = False
    for k,v in regex.items():
        if isinstance(v,list):
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
    if not worked:
        print('no work 8', regex['8'], '\n\n\n')
        for k,v in regex.items():
            if isinstance(v, list):

                # if len(regex[k]) > 20:
                #     break
                # for i, n in enumerate(v):
                #     if n.isdigit():
                #         regex[k] = v[:i] + v
                #         iterative_parse(rx)
                for i, n in enumerate(v):
                    if n.isdigit():
                        regex[k][i] = '+'
                        iterative_parse(rx)

        print('post 8', regex['8'], '\n\n\n')
    return worked


def finish():
    for k, v in regex.items():
        if isinstance(v, list):
            for i in v:
                if i.isdigit():
                    v.remove(i)
        if not any_numbers(v):
            regex[k] = '(' + ''.join(v) + ')'


def p1():
    while iterative_parse(regex):
        pass #print(regex)
    finish()
    while iterative_parse(regex):
        pass
    #print(regex)
    #print('last:', regex['0'])
    ct = 0
    for s in msgs:
        founds = re.findall('^' + regex['0'] + '$', s)
        if len(founds) == 1:
            ct += 1
            # print(founds, regex['0'])

    return ct

print(f'part1: {p1()}')
# print(f'part2: {p2()}')

#260 too low