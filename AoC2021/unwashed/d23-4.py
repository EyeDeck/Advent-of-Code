from collections import *
from aoc import *


def parse_maze(s):
    step = {}
    for y, line in enumerate(s):
        for x, c in enumerate(line):
            if c not in ' #':
                step[x - 1, y - 1] = c.upper()
    return step


def tally_file(f):
    with open(f) as file:
        steps_raw = [[line for line in step.strip().split('\n')] for step in file.read().strip().split('\n\n')]
    steps = []
    for step_raw in steps_raw:
        steps.append(parse_maze(step_raw))
    return tally_path(steps)


def tally_path(steps):
    neighbors = defaultdict(set)
    for k, v in steps[0].items():
        for dir in DIRS:
            d = vadd(dir, k)
            if d in steps[0]:
                neighbors[k].add(d)
    print(neighbors)
    cum = 0
    print_2d(' ', steps[0])
    for i in range(len(steps) - 1):
        a, b = steps[i], steps[i + 1]
        print('->')
        print_2d(' ', b)
        diff = dict(set(b.items()) - set(a.items()))
        swapped = {v: k for k, v in diff.items()}
        # print(swapped)
        src = swapped.pop('.')
        char, tgt = swapped.popitem()
        # print('src, tgt:', src, tgt)
        path = bfs(src, tgt, neighbors)
        cost = (len(path) - 1) * cost_mult[char]
        cum += cost
        print(f'cost:{cost}\tpath:{path}')
        # input()
    return cum


def p1():
    churn(p1_input, p1_tgt, False)
    return None


def churn(graph, tgt, dfs):
    '''
    dfs=True mode is faster to find any answer, but may or may not produce the correct result
    dfs=False should definitely produce the shortest route, but may be much slower
    '''
    active = []
    heapq.heappush(active, (0, getid(), graph.copy()))
    finished = 0
    i = 0
    while len(active):
        i += 1
        if dfs:
            cost, _, cur = active.pop()
        else:
            cost, _, cur = heapq.heappop(active)

        for k, v in cur.items():
            if v == '.' or k == 'cost':
                continue
            # print('aaa', k, v)

            ngh = get_neighbors(cur, k, v)

            if len(ngh) == 0:
                finished += 1
                if cur == tgt:
                    print(cost, '!!!!!!!!')
                    print_2d(' ', cur)
                    return cost, cur
                continue

            # print_2d(' ', cur, {k: 'X'})
            # print(f'cost {cost} got ngh:')
            # print_2d(' ', cur, {k: 'X' for k in ngh})

            for n in ngh:
                if n == k:
                    continue
                new_cost = (abs(n[0] - k[0]) + abs(n[1] - k[1])) * cost_mult[v]
                new_graph = cur.copy()
                new_graph[k] = '.'
                new_graph[n] = v
                if dfs:
                    active.append((cost + new_cost, getid(), new_graph))
                else:
                    heapq.heappush(active, (cost + new_cost, getid(), new_graph))
        if i % 1000 == 0:
            print('new len of active:', len(active), 'finished (dead paths):', finished)
            if dfs:
                print_2d(' ', active[-1][2])
            else:
                print_2d(' ', active[0][2])
        # input()


def p2():
    # p2_input['cost'] = 0
    churn(p2_input, p2_tgt, True)
    return None


def get_connected_empty(graph, node):
    # print('looking for .s')
    heads = [node]
    nodes = set()
    while len(heads) > 0:
        c = heads.pop()
        for dir in DIRS:
            n = vadd(dir, c)
            # print('checking at', n)
            # if n in graph:
            #     print('neighbor', n, '=', graph[n])
            if n not in nodes and n in graph and graph[n] == '.':
                nodes.add(n)
                heads.append(n)
    # print('found', nodes)
    return nodes


def get_neighbors(graph, node, label):
    x, y = node

    # print(f'got these connected nodes to {graph[node]} at {node}: {connected}')
    if y == 0:
        connected = get_connected_empty(graph, node)
        # we're on the top row, so can _only_ go down--filter valid columns
        potential_spots = {x for x in connected if x in cols if x in cols_per_letter[label]}
        if len(potential_spots) == 0:
            return {}
        # print('potential spots:', potential_spots)
        # print_2d(' ', graph)
        for coord in cols_per_letter[label]:
            if coord in graph and graph[coord] != label:
                if graph[coord] == '.':
                    return {coord}
                else:
                    return {}
        die()
    else:
        # we're in a column, so can only go up--filter connected upper row spots
        this_col = cols_per_letter[label]
        if node in this_col:
            frozen = False
            for coord in this_col:
                if coord == node:
                    frozen = True
                    break
                elif coord in graph and graph[coord] != label:
                    break
            if frozen:
                # print('we frozen?')
                # input()
                return {}
        connected = get_connected_empty(graph, node)
        return {x for x in connected if x in top}


def getid():
    global counter
    counter += 1
    return counter


top = {(0, 0), (1, 0), (3, 0), (5, 0), (7, 0), (9, 0), (10, 0)}
cols = {
    (2, 1), (4, 1), (6, 1), (8, 1),
    (2, 2), (4, 2), (6, 2), (8, 2),
    (2, 3), (4, 3), (6, 3), (8, 3),
    (2, 4), (4, 4), (6, 4), (8, 4)
}
cols_per_letter = {
    'A': [(2, 4), (2, 3), (2, 2), (2, 1)],
    'B': [(4, 4), (4, 3), (4, 2), (4, 1)],
    'C': [(6, 4), (6, 3), (6, 2), (6, 1)],
    'D': [(8, 4), (8, 3), (8, 2), (8, 1)]
}
cost_mult = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
counter = 0

day = 23
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    p1_raw = [line.strip('\n') for line in file.readlines()]
    p2_extra = '  #D#C#B#A#\n  #D#B#A#C#'
    p1_input = parse_maze(p1_raw)
    p2_input = parse_maze(p1_raw[:3] + p2_extra.split('\n') + p1_raw[3:])

p1_tgt = '''#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########'''.split('\n')

p2_tgt = '''#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########'''.split('\n')

p1_tgt = parse_maze(p1_tgt)
p2_tgt = parse_maze(p2_tgt)

print(p2_input)

print_2d(' ', p1_input)
print_2d(' ', p2_input)

# print(tally_file('d23p2e.txt'))

print(f'part1: {p1()}')
print(f'part2: {p2()}')
