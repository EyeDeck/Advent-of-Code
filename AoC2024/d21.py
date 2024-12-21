import itertools

from aoc import *
import networkx as nx


def p1():
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
                # print(G, k, v, n, d[n])
        return G

    num_pad_graph = make_graph(num_pad)
    dir_pad_graph = make_graph(dir_pad)
    # print(num_pad_graph)
    # print(dir_pad_graph)

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
                print(path)
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
        best_path = ''
        for possibility in itertools.product(*optimized_possibilities):
            possibility = 'A' + ''.join(possibility)
            three = ''.join([keypad_map[possibility[i]][possibility[i + 1]] for i in range(len(possibility) - 1)])
            if len(three) < shortest:
                shortest = len(three)
                best_path = three
            shortest = min(shortest, len(three))
        print(best_path)

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


# keypad_map = {
#     '^': {'^': 'A', 'A': '>A', 'v': 'vA', '<': 'v<A', '>': ['v>A', '>vA']},
#     'A': {'A': 'A', '^': '<A', 'v': ['v<A', '<vA'], '<': 'v<<A', '>': 'vA'},
#     '<': {'<': 'A', 'A': '>>^A', '^': '>^A', 'v': '>A', '>': '>>A'},
#     'v': {'v': 'A', 'A': ['^>A', '>^A'], '^': '^A', '<': '<A', '>': '>A'}
#     '>': {'>': 'A', 'A': '^A', '^': ['<^A', '^<A'], 'v': '<A', '<': '<<A'},
# }

keypad_map = {
    '^': {'^': 'A', 'A': '>A',   'v': 'vA',  '<': 'v<A',  '>': 'v>A'},
    'A': {'A': 'A', '^': '<A',   'v': '<vA', '<': 'v<<A', '>': 'vA'},
    '<': {'<': 'A', 'A': '>>^A', '^': '>^A', 'v': '>A',   '>': '>>A'},
    'v': {'v': 'A', 'A': '>^A',  '^': '^A',  '<': '<A',   '>': '>A'},
    '>': {'>': 'A', 'A': '^A',   '^': '<^A', 'v': '<A',   '<': '<<A'}
}

keypad_map2 = {
    '^': {'^': 'A', 'A': '>A', 'v': 'vA', '<': 'v<A', '>': ['v>A', '>vA']},
    'A': {'A': 'A', '^': '<A', 'v': ['v<A', '<vA'], '<': 'v<<A', '>': 'vA'},
    '<': {'<': 'A', 'A': '>>^A', '^': '>^A', 'v': '>A', '>': '>>A'},
    'v': {'v': 'A', 'A': ['^>A', '>^A'], '^': '^A', '<': '<A', '>': '>A'},
    '>': {'>': 'A', 'A': '^A', '^': ['<^A', '^<A'], 'v': '<A', '<': '<<A'}
}


def p2():


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
                # print(G, k, v, n, d[n])
        return G

    num_pad_graph = make_graph(num_pad)

    @memo
    def min_steps(a, b, n):
        poss = keypad_map[a][b]
        if n == 0:
            return len(poss)

        poss = 'A' + poss
        # print('POSS', poss)
        total = 0
        for i in range(len(poss) - 1):
            total += min_steps(poss[i], poss[i + 1], n - 1)
        # print('returning', total, 'for', a, 'to', b)
        return total

    @memo
    def min_steps(fro, to, n):
        posses = keypad_map2[fro][to]
        if not isinstance(posses, list):
            posses = [posses]
        if n == 0:
            return min(len(s) for s in posses)

        totals = []
        for piss in posses:
            piss = 'A' + piss
            # print('PISS', piss)
            total = 0
            for i in range(len(piss) - 1):
                total += min_steps(piss[i], piss[i + 1], n - 1)
            # print('returning', total, 'for', fro, to, n)
            totals.append(total)
        return min(totals)


    acc = 0
    for line in data:
        print(line)
        line = 'A' + line
        numpad_steps = [(line[i], line[i + 1]) for i in range(len(line) - 1)]
        # print(numpad_steps)
        expanded_steps = []
        best = []
        step_total = 0
        for numpad_step in numpad_steps:
            # print()
            # expanded_steps.append()
            paths = []
            # print('shortest paths from', numpad_step)
            for digit_path in nx.all_shortest_paths(num_pad_graph, *numpad_step):
                # path = [num_pad_graph[digit_path[i]][digit_path[i + 1]]["dir"] for i in range(len(digit_path) - 1)]
                path = 'A' + ''.join(num_pad_graph[digit_path[i]][digit_path[i + 1]]["dir"] for i in range(len(digit_path) - 1))
                # print(path)
                # path.append('A')
                # path.insert(0, 'A')

                # print(digit_path, path)
                # paths.append(''.join([keypad_map[path[i]][path[i+1]] for i in range(len(path) - 1)]))
                # print([[path[i], path[i+1]] for i in range(len(path)-1)])
                paths.append(path)
            # print(paths)
            expanded_steps.append(paths)
            # best.append(min(paths, key=len))
        # print(f'possibilities for {line}:')
        # print('ex_steps', expanded_steps)
        # expanded_steps = [min(n) for n in expanded_steps]
        # print(expanded_steps)
        # print()
        # step_total = sum(expanded_steps)

        shortest = INF
        for possibility in itertools.product(*expanded_steps):
            possibility = ''.join(possibility) + 'A'
            # print('possibility!', possibility)
            sums = [min_steps(possibility[i], possibility[i + 1], 24) for i in range(len(possibility) - 1)]
            # print(sums)
            this_n = sum(sums)
            shortest = min(shortest, this_n)
        #     three = ''.join([keypad_map[possibility[i]][possibility[i + 1]] for i in range(len(possibility) - 1)])
        #     if len(three) < shortest:
        #         shortest = len(three)
        #         best_path = three
        #     shortest = min(shortest, len(three))
        # print(best_path)

        # sum([min_steps(path[i], path[i + 1], 2) for i in range(len(path) - 1)])

        # optimized_possibilities = []
        # for list_of_possiblities in expanded_steps:
        #     # print(list_of_possiblities)
        #     mn = len(min(list_of_possiblities, key=len))
        #     optimized_possibilities.append([l for l in list_of_possiblities if len(l) == mn])
        #     # print(mn)
        #
        # print(f'possibilities for {line[1:]}:')
        # print(optimized_possibilities)
        #
        #
        #
        # print(min_steps('^', '>', 25))
        #
        # shortest = INF
        # for possibility in itertools.product(*optimized_possibilities):
        #     possibility = 'A' + ''.join(possibility)
        #     three = ''.join([keypad_map[possibility[i]][possibility[i + 1]] for i in range(len(possibility) - 1)])
        #     print(three)
        #     shortest = min(shortest, len(three))

        num_part = int(''.join(re.findall(r'\d', line)))
        acc += num_part * shortest  #shortest


    return acc


setday(21)

data = parselines()
# data = [data[0]]

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
# print(num_pad, dir_pad)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

# print('part1:', p1())
print('part2:', p2())

# print('part1: %d\npart2: %d' % solve())
