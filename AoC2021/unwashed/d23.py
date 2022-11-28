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


def churn(graph, tgt, rev=False):
    active = []
    seen_states = {}
    ignore_ids = set()
    if rev:
        heapq.heappush(active, (0, 0, getid(), graph.copy()))
    else:
        heapq.heappush(active, (0, getid(), graph.copy()))
    i = 0
    while len(active):
        i += 1
        if rev:
            wasted, cost, state_id, cur = heapq.heappop(active)
        else:
            cost, state_id, cur = heapq.heappop(active)

        if state_id in ignore_ids:
            ignore_ids.remove(state_id)
            continue

        for k, v in cur.items():
            if v == '.' or k == 'cost':
                continue

            ngh = get_neighbors(cur, k, v)

            if len(ngh) == 0:
                if cur == tgt:
                    print(i)
                    return cost, cur
                continue

            # print_2d(' ', cur, {k: 'X'})
            # print(f'cost:{cost}, wasted:{wasted}, neighbors:')
            # print_2d(' ', cur, {k: 'X' for k in ngh} | {k: v.lower()})
            # input()

            for n in ngh:
                new_cost = ((abs(n[0] - k[0]) + abs(n[1] - k[1])) * cost_mult[v]) + cost

                new_graph = cur.copy()
                new_graph[k] = '.'
                new_graph[n] = v
                new_id = getid()

                hashable = tuple(sorted(new_graph.items()))
                if hashable in seen_states:
                    prev_cost, prev_id = seen_states[hashable]
                    if prev_cost <= new_cost:
                        # equal or better path to this state already known
                        continue
                    if prev_cost > new_cost:
                        ignore_ids.add(prev_id)
                        seen_states[hashable] = (new_cost, new_id)
                else:
                    seen_states[hashable] = (new_cost, new_id)

                if rev:
                    c = cols_per_letter[v][3]  # top of destination column

                    # the path this is taking
                    path_from_start_to_next = bfs(k, n, cur, True)
                    # theoretically optimal path
                    path_from_start_to_dest = bfs(k, c, cur, False)

                    path_from_start_to_next.pop()

                    optimal_path = set(path_from_start_to_dest[:-1])
                    cst = 0
                    for z in path_from_start_to_next:
                        if z not in optimal_path:
                            cst += 1

                    this_wasted = cst # * cost_mult[v]
                    new_wasted = this_wasted + wasted

                if rev:
                    heapq.heappush(active, (new_wasted, new_cost, new_id, new_graph))
                else:
                    heapq.heappush(active, (new_cost, new_id, new_graph))
        # if i % 1000 == 0:
        #     to_print = active[0]
        #     print(f'len active:{len(active)}, wasted:{to_print[0]}, cost:{to_print[1]}, ignores: len {len(ignore_ids)}')
        #     print_2d(' ', to_print[3])


def bfs(src, tgt, graph, open=True):
    q = deque([src])

    parent = {}

    while q:
        cur = q.popleft()
        if cur == tgt:
            break

        for dir in DIRS:
            n = vadd(dir, cur)
            if n not in graph:
                continue
            if open and graph[n] != '.':
                continue

            if n in parent:
                continue
            parent[n] = cur
            q.append(n)

    if tgt not in parent:
        return [src]

    pos = tgt
    path = []
    while pos != src:
        path.append(pos)
        pos = parent[pos]
    path.append(src)
    path.reverse()
    return path


def get_connected_empty(graph, node):
    heads = [node]
    nodes = set()
    while len(heads) > 0:
        c = heads.pop()
        for dir in DIRS:
            n = vadd(dir, c)
            if n not in nodes and n in graph and graph[n] == '.':
                nodes.add(n)
                heads.append(n)
    return nodes


def get_neighbors(graph, node, label):
    if node[1] == 0:
        connected = get_connected_empty(graph, node)
        # we're on the top row, so can _only_ go down--filter valid columns
        potential_spots = {n for n in connected if n in cols if n in cols_per_letter[label]}
        if len(potential_spots) == 0:
            return {}
        for coord in cols_per_letter[label]:
            if coord in graph and graph[coord] != label:
                if graph[coord] == '.':
                    return {coord}
                else:
                    return {}
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
                return {}
        connected = get_connected_empty(graph, node)
        return {x for x in connected if x in top}


def getid():
    global counter
    counter += 1
    return counter


def p1():
    return churn(p1_input, p1_tgt, True)[0]


def p2():
    return churn(p2_input, p2_tgt)[0]


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

# print(p2_input)

# print_2d(' ', p1_input)
# print_2d(' ', p2_input)

# print(tally_file('d23a-hand.txt'))
# input()

# I solved part 1 by hand before writing code that could do it, but couldn't
# work out part 2, so ended up writing this shitty program
# It was much harder to get part 1 code working than part 2
print('running part 1...', end='\r')
print(f'part1: {p1()}' + ' ' * 100)
print('running part 2...', end='\r')
print(f'part2: {p2()}' + ' ' * 100)
