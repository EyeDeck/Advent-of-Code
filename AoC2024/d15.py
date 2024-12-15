from aoc import *


def parse_puzzle(raw):
    grid = {}
    inverse = defaultdict(list)
    unique = {}
    non_unique = set()

    for y, line in enumerate(raw.split('\n')):
        line = line.strip()
        for x, c in enumerate(line):
            grid[x, y] = c

            inverse[c].append((x, y))

            if c in unique:
                del unique[c]
                non_unique.add(c)
            elif c not in non_unique:
                unique[c] = (x, y)

    for k in inverse['.']:
        del grid[k]

    return grid, unique['@']


def p1():
    grid, robot = parse_puzzle(grid_raw)

    for move in movements:
        dir = DIR_MAP[move]
        next_pos = robot_next_pos = vadd(robot, dir)
        stack = [('@', robot)]
        while True:
            if next_pos not in grid:
                break
            elif grid[next_pos] == 'O':
                stack.append((grid[next_pos], next_pos))
                next_pos = vadd(next_pos, dir)
            elif grid[next_pos] == '#':
                robot_next_pos = None
                stack = []
                break

        if robot_next_pos is None:
            continue

        robot = robot_next_pos

        for object in stack:
            del grid[object[1]]

        for object in stack:
            grid[vadd(object[1], dir)] = object[0]

        if verbose:
            print_2d('.', grid)

    boxes = {k: k for k, v in grid.items() if v == 'O'}
    return sum((k[0] + (k[1] * 100)) for k in boxes)


def p2():
    grid_raw_doubled = grid_raw.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')

    grid, robot = parse_puzzle(grid_raw_doubled)

    for move in movements:
        dir = DIR_MAP[move]
        robot_next_pos = vadd(robot, dir)
        seen = {}
        frontier = {robot: '@'}
        while frontier:
            next_pos = vadd(frontier.popitem()[0], dir)
            if next_pos not in grid:
                continue
            next_tile = grid[next_pos]
            if next_tile in '[]':
                frontier[next_pos] = next_tile

                if next_tile == '[' and dir != (-1, 0):
                    other_piece = vadd(next_pos, (1, 0))
                elif next_tile == ']' and dir != (1, 0):
                    other_piece = vadd(next_pos, (-1, 0))
                else:
                    continue
                frontier[other_piece] = grid[other_piece]

            elif next_tile == '#':
                robot_next_pos = None
                break

            seen.update(frontier)

        if robot_next_pos is None:
            continue

        robot = robot_next_pos

        for k in seen:
            del grid[k]

        for k, v in seen.items():
            grid[vadd(k, dir)] = v

        if verbose:
            print_2d('.', grid)

    boxes = {k: k for k, v in grid.items() if v == '['}
    return sum((k[0] + (k[1] * 100)) for k in boxes)


setday(15)

with open_default() as file:
    grid_raw, movements = file.read().split('\n\n')

movements = movements.replace('\n', '')

DIR_MAP = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())
