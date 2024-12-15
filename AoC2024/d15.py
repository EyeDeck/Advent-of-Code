from aoc import *


def p1():
    grid = {}
    inverse = defaultdict(list)
    unique = {}
    non_unique = set()

    for y, line in enumerate(grid_raw.split('\n')):
        line = line.strip()
        for x, c in enumerate(line):
            grid[x, y] = c

            inverse[c].append((x, y))

            if c in unique:
                del unique[c]
                non_unique.add(c)
            elif c not in non_unique:
                unique[c] = (x, y)

    print(grid, movements)
    print_2d('.', grid)
    robot = unique['@']

    for k in inverse['.']:
        del grid[k]
    print_2d(' ', grid)

    dir_map = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}

    for move in movements:
        dir = dir_map[move]
        next_pos = robot_next_pos = vadd(dir, robot)
        stack = [('@', robot)]
        while True:
            if next_pos not in grid:
                break
            elif grid[next_pos] == 'O':
                stack.append((grid[next_pos], next_pos))
                next_pos = vadd(next_pos, dir)
                print(next_pos)
            elif grid[next_pos] == '#':
                robot_next_pos = None
                stack = []
                break

        print(move, stack)
        if robot_next_pos != None:
            robot = robot_next_pos

        for object in stack:
            del grid[object[1]]

        for object in stack:
            grid[vadd(object[1], dir)] = object[0]

        if verbose:
            print_2d('.', grid)

    boxes = {k: k for k, v in grid.items() if v == 'O'}
    # print_2d('.     ', boxes)
    return sum((k[0] + (k[1] * 100)) for k in boxes)


def p2():
    grid_raw_doubled = grid_raw.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
    print(grid_raw_doubled)

    grid = {}
    inverse = defaultdict(list)
    unique = {}
    non_unique = set()

    for y, line in enumerate(grid_raw_doubled.split('\n')):
        line = line.strip()
        for x, c in enumerate(line):
            grid[x, y] = c

            inverse[c].append((x, y))

            if c in unique:
                del unique[c]
                non_unique.add(c)
            elif c not in non_unique:
                unique[c] = (x, y)

    print(grid, movements)
    print_2d('.', grid)
    robot = unique['@']

    for k in inverse['.']:
        del grid[k]
    print_2d(' ', grid)

    dir_map = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}

    for move in movements:
        dir = dir_map[move]
        next_pos = robot_next_pos = vadd(dir, robot)
        old_frontier = set()
        frontier = {('@', robot)}
        while frontier:
            # print(frontier)
            # print(old_frontier)
            # input()
            new_frontier = set()
            for coord in frontier:
                if coord in old_frontier:
                    continue
                next_pos = vadd(coord[1], dir)
                if next_pos not in grid:
                    continue
                elif grid[next_pos] in '[]':
                    new_frontier.add((grid[next_pos], next_pos))

                    if grid[next_pos] == '[':
                        other_piece = vadd(next_pos, (1, 0))
                    else:
                        other_piece = vadd(next_pos, (-1, 0))
                    new_frontier.add((grid[other_piece], other_piece))

                    # print(next_pos)
                elif grid[next_pos] == '#':
                    print('wall!')
                    robot_next_pos = None
                    new_frontier = set()
                    frontier = set()
                    old_frontier = set()
                    break

            old_frontier.update(frontier)
            frontier = new_frontier

        print(move, old_frontier)
        if robot_next_pos is not None:
            robot = robot_next_pos

        for object in old_frontier:
            del grid[object[1]]

        for object in old_frontier:
            grid[vadd(object[1], dir)] = object[0]

        if verbose:
            print_2d('.', grid)
            input()

    boxes = {k: k for k, v in grid.items() if v == '['}
    # print_2d('.     ', boxes)
    return sum((k[0] + (k[1] * 100)) for k in boxes)


setday(15)

with open_default() as file:
    grid_raw, movements = file.read().split('\n\n')

movements = ''.join(movements.split('\n'))

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1() )
print('part2:', p2() )
