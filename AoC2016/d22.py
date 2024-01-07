import copy
from aoc import *


def p1():
    acc = 0
    for a, a_info in nodes.items():
        for b, b_info in nodes.items():
            if a == b:
                continue
            if a_info[1] == 0:
                continue
            if a_info[1] <= b_info[2]:
                acc += 1
    return acc


def p2():
    # print(nodes)
    acc = 0

    walls = set()
    for node, info in nodes.items():
        # neighbors = [vadd(node, d) for d in DIRS]
        # # print(neighbors)
        # neighbors = [nodes[n] for n in neighbors if n in nodes and type(nodes[n]) == list]
        # print(node, [info[1] > n[0] for n in neighbors])
        # if all(info[1] > n[0] for n in neighbors):
        #     print(node, 'wall')
        #     nodes[node] = '#'
        if info[1] > 300:
            walls.add(node)
    for key in walls:
        del nodes[key]
    neighbors = {}
    for node, info in nodes.items():
        n = [n for n in [vadd(node, d) for d in DIRS] if n in nodes]
        neighbors[node] = n
    # print(neighbors)

    goal = (max(nodes.keys())[0], 0)
    print(goal)
    def find_empty():
        for node, info in nodes.items():
            if info[1] == 0:
                return node

    acc = 0
    # print({k:'.' if v is type(list) else v for k,v in nodes.items()})
    empty = find_empty()

    route = bfs(empty, vadd(goal, (-1,0)), neighbors)
    print_2d('   ', {k:' .' for k,v in nodes.items()}, {k:' ~' for k in route}, {(0,0):'(.)', goal:' G', empty:' _'})
    print(route)

    def shift_route(route):
        print(route, [nodes[n] for n in route])
        steps = 0
        for i in range(len(route)-1):
            a, b = route[i], route[i+1]
            an, bn = nodes[a], nodes[b]
            assert an[1] == 0
            assert bn[1] <= an[0]
            an[1], bn[1] = bn[1], an[1]
            print(a, an, b, bn)
            steps += 1
        return steps

    acc += shift_route(route)

    empty = find_empty()

    print_2d('   ', {k: ' .' for k, v in nodes.items()}, {(0, 0): '(.)', goal: ' G', find_empty(): ' _'})
    print('new empty at', empty)

    while True:
        prev_goal, goal = goal, vadd(goal, (-1,0))
        print(prev_goal, goal)
        nodes[prev_goal][1], nodes[goal][1] = nodes[goal][1], nodes[prev_goal][1]
        acc += 1
        if goal == (0,0):
            break
        next_neighbors = copy.deepcopy(neighbors)
        for n in next_neighbors[goal]:
            next_neighbors[n].remove(goal)
            # print(n)
        empty = vadd(goal, (-1,0))
        route = bfs(prev_goal, empty, next_neighbors)
        acc += shift_route(route)

        print_2d('   ', {k: ' .' for k, v in nodes.items()}, {k:' ~' for k in route}, {(0, 0): '(.)', goal: ' G', find_empty(): ' _'})

    return acc


setday(22)

data = parselines()

r = re.compile(r'(\d+)+')
nodes = {}
for line in data:
    rx = [int(n) for n in re.findall(r, line)]
    if not rx:
        continue
    x, y, size, used, avail, pct = rx
    nodes[(x, y)] = [size, used, avail, pct]

print('part1:', p1() )
print('part2:', p2() )
