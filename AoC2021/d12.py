import sys
from collections import *


def getneighbors(path, graph):
    head = path[-1]
    potential = graph[head]
    # print('found:', path, potential)
    return [p for p in potential if not (p.islower() and p in path)]


def getneighbors2(path, graph):
    head = path[-1]
    potential = graph[head]
    # print('found:', path, potential)
    small2 = True
    for p in path:
        if not p.islower():
            continue
        if path.count(p) == 2:
            small2 = False
            break
    return [p for p in potential if small2 or not (p.islower() and p in path)]


def bfs(src, tgt, neighbors, nfunc):
    q = deque([[src]])
    done = []
    while q:
        cur = q.popleft()
        head = cur[-1]
        if head == tgt:
            done.append(cur)
            continue
        nbrs = nfunc(cur, neighbors)
        for n in nbrs:
            newpath = cur.copy()
            newpath.append(n)
            q.append(newpath)
    return done


def p1():
    x = bfs('start', 'end', connections, getneighbors)
    return len(x)


def p2():
    x = bfs('start', 'end', connections, getneighbors2)
    # for y in sorted(x):
    #    print(y)
    return len(x)


day = 12
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip().split('-') for line in file]
    connections = defaultdict(set)
    for line in data:
        a, b = line
        if b != 'start':
            connections[a].add(b)
        if a != 'start':
            connections[b].add(a)
    # print(connections)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
