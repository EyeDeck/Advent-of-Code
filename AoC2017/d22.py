from aoc import *


def p1():
    heading = 1
    board = {k for k, v in grid.items() if v == '#'}
    pos = tuple((i // 2) for i in grid_bounds(grid)[2:])
    if verbose and v1:
        print('starting pos:', pos, 'grid bounds:', grid_bounds(grid)[2:])

    acc = 0
    for burst in range(10000):
        if verbose and v1:
            print('h', heading, 'p', pos)
            print_2d('. ', {k: '#' for k in board}, {pos: '@'})
            input()

        cur_infected = pos in board
        heading = (heading + (-1 if cur_infected else 1)) % 4
        if cur_infected:
            board.remove(pos)
        else:
            acc += 1
            board.add(pos)
        pos = vadd(pos, DIRS[heading])

    return acc


def p2():
    heading = 1
    board = defaultdict(int, {k: 2 for k, v in grid.items() if v == '#'})
    pos = tuple((i // 2) for i in grid_bounds(grid)[2:])
    if verbose and v2:
        print('starting pos:', pos, 'grid bounds:', grid_bounds(grid)[2:])

    acc = 0
    for burst in range(10000000):
        if verbose and v2:
            print('h', heading, 'p', pos)
            print_2d_repl('. ',
                          [{k: v for k, v in board.items()}, {0: '.', 1: 'W', 2: '#', 3: 'F',}],
                          [{pos: '@'}, {}])

            input()

        cur = board[pos]
        if cur == 0:
            heading += 1
        elif cur == 1:
            acc += 1
        elif cur == 2:
            heading -= 1
        elif cur == 3:
            heading += 2

        heading %= 4
        board[pos] = (board[pos] + 1) % 4

        pos = vadd(pos, DIRS[heading])
    return acc


setday(22)

grid, inverse, unique = parsegrid()

verbose = '-v' in sys.argv or '--verbose' in sys.argv
v1, v2 = '1' in sys.argv, '2' in sys.argv

print('part1:', p1())
print('part2:', p2())
