import math
import operator
from aoc import *


def p1():
    acc = 0
    for part in ratings:
        cur = 'in'
        while cur not in ['A', 'R']:
            for thing in workflows[cur][:-1]:
                # print('thing', thing)
                if thing[0](part[thing[1]], thing[2]):
                    cur = thing[3]
                    break
            else:
                cur = workflows[cur][-1]
            # print(part, cur, workflows[cur] if cur in workflows else '')
            # input()
        if cur == 'A':
            acc += sum(part.values())
    return acc


def p2():
    acc = 0
    stack = [['in', {k:(1,4000) for k in 'xmas'}]]
    while stack:
        print('STACK', stack)
        cur = stack.pop()
        print('POPPED', cur)
        if cur[0] == 'A':
            print(cur[1])
            s = math.prod((r[1]-r[0]+1) for r in cur[1].values())
            print('acc', s)
            acc += s
            continue
        elif cur[0] == 'R':
            continue

        print(cur)
        rng = cur[1].copy()
        for rule in workflows[cur[0]][:-1]:
            new_rng = rng.copy()
            func, v, n, dest = rule
            print(v, n)
            if func == operator.gt:
                if rng[v][0] > n:
                    print('out of range (gt)')
                    continue

                print('gt', n, rng[v][0])
                new_rng[v] = (min(n+1,rng[v][1]), rng[v][1])
                print('new_rng', new_rng)
                # rng[v] = (rng[v][0], min(rng[v][1], n))
                rng[v] = (rng[v][0], min(n,rng[v][1]))
                print('after mod gt', rng[v])
                stack.append([dest, new_rng])
            elif func == operator.lt:
                if rng[v][1] < n:
                    print('out of range (lt)')
                    continue

                new_rng[v] = (rng[v][0], min(n-1,rng[v][1]))
                print('new_rng', new_rng)
                # rng[v] = (min(rng[v][0], n), rng[v][1])
                rng[v] = (min(n,rng[v][1]), rng[v][1])
                print('after mod lt', rng[v][0], n, min(rng[v][0], n)) # )v, rng[v][0], rng[v][1], n, min(rng[v][0], n), rng[v][1])
                stack.append([dest, new_rng])
        stack.append([workflows[cur[0]][-1],rng.copy()])
        # input()
    return acc


setday(19)


with open_default() as file:
    data = [line.strip() for line in file.read().split('\n\n')]
workflows_raw, ratings_raw = [line.split('\n') for line in data]

workflows = {}
for workflow in workflows_raw:
    name, rest = workflow.split('{')
    rest = rest[:-1]
    rest = rest.split(',')
    rules = []
    for part in rest:
        if '<' in part:
            a, b = part.split('<')
            b, c = b.split(':')
            rules.append([operator.lt, a, int(b), c])
        elif '>' in part:
            a, b = part.split('>')
            b, c = b.split(':')
            rules.append([operator.gt, a, int(b), c])
        else:
            rules.append(part)
    workflows[name] = rules
    # print(name, rest)

ratings = []
for line in [line[1:-1].split(',') for line in ratings_raw]:
    d = {}
    # print(line)
    for part in line:
        parts = part.split('=')
        d[parts[0]] = int(parts[1])
    ratings.append(d)

print('part1:', p1() )
print('part2:', p2() )
