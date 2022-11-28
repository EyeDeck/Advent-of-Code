import sys
from collections import *


def solve():
    paths = deque([(0, [k]) for k in graph.keys()])
    finished = []
    node_count = len(graph)
    while paths:
        dist, path = paths.pop()
        if len(path) == node_count:
            finished.append((dist, path))
        for k, v in graph[path[-1]]:
            if k not in path:
                paths.appendleft((dist + v, path + [k]))
    finished = sorted(finished)
    return finished[0][0], finished[-1][0]


day = 9
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

graph = defaultdict(list)
with open(f) as file:
    for line in file:
        a, _, b, _, d = line.split()
        d = int(d)
        graph[a].append((b, d))
        graph[b].append((a, d))
# print(graph)

# print('part1: %s\npart2: %s' % solve())
print('part1: {}\npart2: {}'.format(*solve()))
