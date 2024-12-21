import itertools

from aoc import *
import networkx as nx


def p1():
    def get_all_dists(d):
        rd = defaultdict(dict)
        for k_a, v_a in d.items():
            for k_b, v_b in d.items():
                # print(k_a, v_a, k_b, v_b)
                rd[v_a][v_b] = vdistm(k_a, k_b)
        return rd

    num_pad_dists = get_all_dists(num_pad)
    dir_pad_dists = get_all_dists(dir_pad)
    print(num_pad_dists)
    print(dir_pad_dists)

    # NUMPAD <- DIRPAD <- DIRPAD <- DIRPAD

    def get_neighbors(node, g):
        neighbors = []
        for dir in DIRS:
            n = vadd(node, dir)
            if n in g:
                # print(DIR_MAP)
                neighbors.append((n, DIR_MAP[dir]))
        return neighbors

    def make_graph(d):
        G = nx.DiGraph()
        for k, v in d.items():
            for n, c in get_neighbors(k, d):
                G.add_edge(v, d[n], weight=1, dir=c)
                print(G, k, v, n, d[n])
        return G

    num_pad_graph = make_graph(num_pad)
    dir_pad_graph = make_graph(dir_pad)
    print(num_pad_graph)
    print(dir_pad_graph)

    # for line in data:
    #     print(line)
    #     line = 'A' + line
    #     numpad_steps = [(line[i], line[i+1]) for i in range(len(line)-1)]
    #     print(numpad_steps)
    #     for numpad_step in numpad_steps:
    #         print(numpad_step)
    #         numpad_step_paths = [p for p in nx.all_shortest_paths(num_pad_graph, *numpad_step)]
    #         print(numpad_step_paths)
    #         for numpad_path in numpad_step_paths:
    #             numpad_path_steps = [(numpad_path[i], numpad_path[i + 1]) for i in range(len(numpad_path) - 1)]
    #             print(numpad_path_steps)
    #             for numpad_path_step in numpad_path_steps:
    #                 print(numpad_path_step)
    #                 die()

    acc = 0
    for line in data:
        print(line)
        line = 'A' + line
        numpad_steps = [(line[i], line[i + 1]) for i in range(len(line) - 1)]
        print(numpad_steps)
        expanded_steps = []
        best = []
        for numpad_step in numpad_steps:
            # print()
            # expanded_steps.append()
            paths = []
            print('shortest paths from', numpad_step)
            for digit_path in nx.all_shortest_paths(num_pad_graph, *numpad_step):
                path = [num_pad_graph[digit_path[i]][digit_path[i + 1]]["dir"] for i in range(len(digit_path) - 1)]
                path.append('A')
                path.insert(0, 'A')

                print(digit_path, path)
                paths.append(''.join([keypad_map[path[i]][path[i+1]] for i in range(len(path) - 1)]))
            expanded_steps.append(paths)
            # best.append(min(paths, key=len))
        print(f'possibilities for {line}:')
        print(expanded_steps)

        optimized_possibilities = []
        for list_of_possiblities in expanded_steps:
            print(list_of_possiblities)
            mn = len(min(list_of_possiblities, key=len))
            optimized_possibilities.append([l for l in list_of_possiblities if len(l) == mn])
            print(mn)

        print(f'optimized_possibilities for {line}:')
        print(optimized_possibilities)

        shortest = INF
        for possibility in itertools.product(*optimized_possibilities):
            possibility = 'A' + ''.join(possibility)
            three = ''.join([keypad_map[possibility[i]][possibility[i + 1]] for i in range(len(possibility) - 1)])
            shortest = min(shortest, len(three))

        # print(f'after 2 robots for {line}:')
        # best = ''.join(best)
        # print(best)
        # best = 'A' + best
        # three = ''.join([keypad_map[best[i]][best[i+1]] for i in range(len(best) - 1)])
        # print(f'after 3 robots for {line}:')
        # print(three)
        #
        # # v<A<AA>>^AvAA^<A>Av<<A>>^AvA^Av<A^>A<Av<A>>^AAvA^Av<A<A>>^AAA<A>vA^A
        # # <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
        #
        # print(line, int(''.join(re.findall(r'\d', line))), '*', len(three))
        # acc += int(''.join(re.findall(r'\d', line))) * len(three)
        num_part = int(''.join(re.findall(r'\d', line)))
        acc += num_part * shortest


    return acc

'''
after 3 robots for A980A:
v<<A>>^AAAvA^Av<A<AA>>^AvAA^<A>Av<A<A>>^AAA<A>vA^Av<A^>A<A>A
980A:
<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A

179A:
<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
v<<A>>^Av<A<A>>^AAvAA^<A>Av<<A>>^AAvA^Av<A^>AA<A>Av<A<A>>^AAA<A>vA^A

<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
v<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>A<A>Av<A^>A<A>Av<A<A>>^AA<A>vA^A

v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<A>vA^A
v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<A>vA^A

<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<A>vA^A
'''

# keypad_map = {'^': {'A': '>A', '>': 'v'}
#               }

# keypad_map = {
#     '^': {'^': 'A', 'A': '>A', 'v': 'vA', '<': 'v<A', '>': ['v>A', '>vA']},
#     'A': {'A': 'A', '^': '<A', 'v': ['v<A', '<vA'], '<': 'v<<A', '>': 'vA'},
#     '<': {'<': 'A', 'A': '>>^A', '^': '>^A', 'v': '>A', '>': '>>A'},
#     'v': {'v': 'A', 'A': ['^>A', '>^A'], '^': '^A', '<': '<A', '>': '>A'}
#     '>': {'>': 'A', 'A': '^A', '^': ['<^A', '^<A'], 'v': '<A', '<': '<<A'},
# }

keypad_map = {
    '^': {'^': 'A', 'A': '>A',   'v': 'vA',  '<': 'v<A',  '>': 'v>A'},
    'A': {'A': 'A', '^': '<A',   'v': '<vA', '<': 'v<<A', '>': 'vA' },
    '<': {'<': 'A', 'A': '>>^A', '^': '>^A', 'v': '>A',   '>': '>>A'},
    'v': {'v': 'A', 'A': '>^A',  '^': '^A',  '<': '<A',   '>':  '>A'},
    '>': {'>': 'A', 'A': '^A',   '^': '<^A', 'v': '<A',   '<': '<<A'}
}


# def get_numpad_steps(a, b):
#     steps = []
#     a_x, a,y = num_pad_inv[a]
#     b_x, b_y = num_pad_inv[b]
#     if a_x < b_x:
#
#     elif a_x > b_x:
#         pass
#     return steps


# def p1():
#     for line in data:
#         print(line)
#         line = 'A' + line
#         numpad_steps = [(line[i], line[i+1]) for i in range(len(line)-1)]
#         print(numpad_steps)
#     return None


def p2():
    return None


setday(21)

data = parselines()


def make_pad(s):
    grid = {}
    grid_inv = {}
    for y, line in enumerate(s):
        for x, c in enumerate(line):
            if c != ' ':
                grid[(x, y)] = c
                grid_inv[c] = (x, y)
    return grid, grid_inv


DIR_MAP = {v: k for k, v in {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}.items()}

num_pad, num_pad_inv = make_pad('789,456,123, 0A'.split(','))
dir_pad, dir_pad_inv = make_pad(' ^A,<v>'.split(','))
print(num_pad, dir_pad)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())

# print('part1: %d\npart2: %d' % solve())
