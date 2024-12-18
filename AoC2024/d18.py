from aoc import *


def solve():
    def get_neighbors(node):
        neighbors = []
        for dir in DIRS:
            n = vadd(node, dir)
            if n not in grid and n[0] >= 0 and n[1] >= 0 and n[0] <= WIDTH and n[1] <= HEIGHT:
                neighbors.append((n, 1))
        return neighbors

    grid = {tuple(c) for c in data[:P1_STEPS]}

    result = wbfs(START, TARGET, get_neighbors)

    if verbose:
        print(f'After {P1_STEPS} steps:')
        print_2d('.', {k: '#' for k in grid}, {k: 'O' for k in result})

    p1 = len(result) - 1

    left, mid, right = 0, 0, len(data)
    while left < right:
        mid = (left + right) // 2
        grid = {tuple(c) for c in data[:mid]}

        result = wbfs(START, TARGET, get_neighbors)
        if result is None:
            right = mid
        else:
            left = mid + 1

    if verbose:
        print(f'\nFirst non-traversable grid after {mid} steps:')
        print_2d(' ', {k: '#' for k in grid}, {tuple(data[mid]): '+'})

    p2 = ','.join(str(n) for n in data[mid])

    return p1, p2


setday(18)

data = parselines(get_ints)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

WIDTH, HEIGHT = 70, 70
P1_STEPS = 1024
START, TARGET = (0, 0), (70, 70)

print('part1: %d\npart2: %s' % solve())
