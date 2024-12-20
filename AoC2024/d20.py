from aoc import *


def p1():
    def get_neighbors(node):
        # print('node', node)
        neighbors = []
        pos, cheat = node
        for dir in DIRS:
            # print('loop', pos, cheat, dir)
            n = vadd(pos, dir)
            if n not in grid:
                continue
            if grid[n] != '#':
                # neighbors.append( ((n, (0 if cheat == 1 else cheat)),1))
                neighbors.append(((n, cheat), 1))
            elif cheat >= 1:
                neighbors.append(((n, cheat - 1), 1))
        # print('returning neighbors', neighbors)
        return neighbors

    start = (unique['S'], 1)
    end = (unique['E'], 1)
    # end_cheat = (unique['E'], 0)

    best_path = wbfs(start, end, get_neighbors)
    # print(best_path)
    print_2d('.', grid, {k[0]: 'O' for k in best_path})
    no_cheats = len(best_path) - 1
    print(no_cheats)
    print(best_path)

    diffs = {(2, 0), (0, 2)}
    saves = defaultdict(int)
    search_offset = 98
    for i, first_node in enumerate(best_path):
        # print(i, best_path[i:])
        print(i, end='...\r')
        for j, second_node in enumerate(best_path[i + 1 + search_offset:]):
            a, b = first_node[0], second_node[0]
            m = tuple(n // 2 for n in vadd(a, b))
            # print(m)
            if grid[m] != '#':
                continue
            pos_dist = tuple(abs(i) for i in vsub(a, b))
            # print(pos_dist)
            saved_dist = j - 1 + search_offset
            if pos_dist not in diffs:
                continue
            # print(i,j, first_node, 'skipping to', second_node, 'saving', saved_dist)

            # print()
            # print_2d('.', grid, {k[0]: 'O' for k in best_path[:i+1] + best_path[i+j+1:]}, {a:'A', b:'B'})
            saves[saved_dist] += 1
    print(saves)

    # all_paths = exhaustive_wbfs(start, end_cheat, get_neighbors)
    # print(all_paths)
    # print(len(all_paths))

    return sum(v for k, v in saves.items() if k >= 100)


def p2():
    def get_neighbors(node):
        # print('node', node)
        neighbors = []
        pos = node
        for dir in DIRS:
            # print('loop', pos, cheat, dir)
            n = vadd(pos, dir)
            if n not in grid:
                continue
            if grid[n] != '#':
                # neighbors.append( ((n, (0 if cheat == 1 else cheat)),1))
                neighbors.append((n, 1))
        # print('returning neighbors', neighbors)
        return neighbors

    start = unique['S']
    end = unique['E']
    # end_cheat = (unique['E'], 0)

    best_path = wbfs(start, end, get_neighbors)
    # print(best_path)
    print_2d('.', grid, {k[0]: 'O' for k in best_path})
    no_cheats = len(best_path) - 1
    print(no_cheats)
    print(best_path)

    saves = defaultdict(int)
    search_offset = 20
    for i, first_node in enumerate(best_path):
        # print(i, best_path[i:])
        print(i, end='...\r')
        for j, second_node in enumerate(best_path[i + 1 + search_offset:]):
            path_dist = j - 1 + search_offset
            manhattan_dist = vdistm(first_node, second_node)
            if manhattan_dist > 20:
                continue
            saved_dist = path_dist - manhattan_dist + 2
            if saved_dist < 50:
                continue
            # print(i,j, first_node, 'skipping to', second_node, 'saving', saved_dist)

            # print()
            # print_2d('.', grid, {k[0]: 'O' for k in best_path[:i+1] + best_path[i+j+1:]}, {a:'A', b:'B'})
            saves[saved_dist] += 1
    print(saves)

    for k in sorted(saves.keys()):
        print(f'There are {saves[k]} cheats that save {k} picoseconds.')

    # all_paths = exhaustive_wbfs(start, end_cheat, get_neighbors)
    # print(all_paths)
    # print(len(all_paths))

    return sum(v for k, v in saves.items() if k >= 100)


setday(20)

grid, inverse, unique = parsegrid()

# with open_default() as file:
#     data = get_ints(file.read())

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1() )
print('part2:', p2())

