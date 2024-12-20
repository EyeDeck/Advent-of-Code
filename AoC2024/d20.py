from aoc import *


def solve():
    def get_neighbors(node):
        neighbors = []
        pos = node
        for dir in DIRS:
            n = vadd(pos, dir)
            if n in grid and grid[n] != '#':
                neighbors.append((n, 1))
        return neighbors

    best_path = wbfs(unique['S'], unique['E'], get_neighbors)
    if verbose:
        print_2d('.', grid, {k:'O' for k in best_path})

    saves_p1 = defaultdict(int)
    saves_p2 = defaultdict(int)
    for i, first_node in enumerate(best_path):
        print(i, end='...\r')
        for j, second_node in enumerate(best_path[i + 1 + MIN_SAVE:]):
            path_dist = j - 1 + MIN_SAVE
            manhattan_dist = vdistm(first_node, second_node)

            saved_dist = path_dist - manhattan_dist + 2
            if saved_dist < MIN_SAVE:
                continue

            # if verbose:
            #     print(i,j, first_node, 'skipping to', second_node, 'saving', saved_dist)
            #     print_2d('.', grid, {k[0]: 'O' for k in best_path[:i+1] + best_path[i+j+1:]}, {first_node:'A', second_node:'B'})

            if manhattan_dist <= 2:
                saves_p1[saved_dist] += 1
            if manhattan_dist <= 20:
                saves_p2[saved_dist] += 1

    if verbose:
        for part, d in [['p1:', saves_p1], ['p2:', saves_p2]]:
            for k in sorted(d.keys()):
                print(f'{part} There {f"are {d[k]} cheats" if d[k] > 1 else "is one cheat"} that save{"s" if d[k] == 1 else ""} {k} picoseconds.')

    return sum(v for k, v in saves_p1.items() if k >= MIN_SAVE), sum(v for k, v in saves_p2.items() if k >= MIN_SAVE)


setday(20)

grid, inverse, unique = parsegrid()

verbose = '-v' in sys.argv or '--verbose' in sys.argv

MIN_SAVE = 100

print('part1: %d\npart2: %d' % solve())