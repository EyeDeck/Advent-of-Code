import copy
from itertools import combinations

from ec import *


def p1():
    grid, inverse, unique = parse_grid(1)

    bindings = set()
    for i_label, i_pos in inverse.items():
        print(i_label, i_pos)
        for pos in i_pos:
            for n in [vadd(pos, d) for d in DIRS]:
                if n not in grid or grid[n] != i_label:
                    bindings.add(tuple(sorted([pos, n])))

    return len(bindings)


def p2():
    grid, inverse, unique = parse_grid(2)

    bindings = defaultdict(set)
    # bindings = defaultdict(int)
    for i_label, i_pos in inverse.items():
        print(i_label, i_pos)
        for pos in i_pos:
            for n in [vadd(pos, d) for d in DIRS]:
                if n not in grid:
                    bindings[(i_label, 'frame')].add(tuple(sorted([pos, n])))
                    # bindings[(i_label, 'frame')] += 1
                elif grid[n] != i_label:
                    bindings[tuple(sorted([i_label, grid[n]]))].add(tuple(sorted([pos, n])))
                    # bindings[tuple(sorted([i_label, grid[n]]))] += 1

    for k, v in bindings.items():
        print(k, v)

    acc = 0
    bound = {'frame',}
    while bindings:
        shortest_label, shortest_ct = None, INF
        for k, v in bindings.items():
            len_v = len(v)
            a, b = k
            if a in bound:
                if len_v < shortest_ct:
                    shortest_label, shortest_ct = k, len_v
            elif b in bound:
                if len_v < shortest_ct:
                    shortest_label, shortest_ct = k, len_v

        a, b = shortest_label
        if a in bound:
            bound.add(b)
        else:
            bound.add(a)
        bindings.pop(shortest_label)

        acc += shortest_ct
        print('bound', shortest_label, 'with len', shortest_ct)

        to_clean = []
        for k, v in bindings.items():
            a, b = k
            if a in bound and b in bound:
                to_clean.append(k)

        print('to clean', to_clean)
        for k in to_clean:
            bindings.pop(k)
        print('cleaned', to_clean)


    return acc


def p3():
    grid, inverse, unique = parse_grid(3)

    bindings = defaultdict(set)
    # bindings = defaultdict(int)
    for i_label, i_pos in inverse.items():
        print(i_label, i_pos)
        for pos in i_pos:
            for n in [vadd(pos, d) for d in DIRS]:
                if n not in grid:
                    bindings[(i_label, 'frame')].add(tuple(sorted([pos, n])))
                    # bindings[(i_label, 'frame')] += 1
                elif grid[n] != i_label:
                    bindings[tuple(sorted([i_label, grid[n]]))].add(tuple(sorted([pos, n])))
                    # bindings[tuple(sorted([i_label, grid[n]]))] += 1

    for k, v in bindings.items():
        print(k, v)

    bindings_org = bindings

    best = INF
    for spell_shots in combinations(inverse, 2):
        print(spell_shots)
        bindings = copy.deepcopy(bindings_org)

        bound = {'frame',*spell_shots}

        bindings_to_pop = set()
        for k, v in bindings.items():
            a, b = k
            if a in spell_shots:
                bindings_to_pop.add(k)
                bound.add(b)
            if b in spell_shots:
                bindings_to_pop.add(k)
                bound.add(a)
        for k in bindings_to_pop:
            bindings.pop(k)

        acc = 0
        while bindings:
            to_clean = []
            for k, v in bindings.items():
                a, b = k
                if a in bound and b in bound:
                    to_clean.append(k)

            # print('to clean', to_clean)
            for k in to_clean:
                bindings.pop(k)

            if len(bindings) == 0:
                break

            shortest_label, shortest_ct = None, INF
            for k, v in bindings.items():
                len_v = len(v)
                a, b = k
                if a in bound:
                    if len_v < shortest_ct:
                        shortest_label, shortest_ct = k, len_v
                elif b in bound:
                    if len_v < shortest_ct:
                        shortest_label, shortest_ct = k, len_v

            a, b = shortest_label
            if a in bound:
                bound.add(b)
            else:
                bound.add(a)
            bindings.pop(shortest_label)

            acc += shortest_ct
            # print('bound', shortest_label, 'with len', shortest_ct)


            # print('cleaned', to_clean)
        if acc < best:
            best = acc

    return best


if __name__ == '__main__':
    setquest(14)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
