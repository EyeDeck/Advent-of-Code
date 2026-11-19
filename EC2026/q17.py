from ec import *


def p1():
    grid, inverse, unique = parse_grid(1)
    start, end = min(grid), max(grid)

    neighbors = pregen_neighbors(grid, DIRS,'.')
    route = bfs(start, end, neighbors)

    if verbose:
        print_2d(' ', grid, {k:'~' for k in route})
    return len(route)-1


def p2():
    grid, inverse, unique = parse_grid(2)

    acc = 0
    for point in grid:
        if grid[point] != '#':
            continue
        for d in DIRS:
            p = vadd(d, point)
            if p not in grid or grid[p] == '.':
                acc += 1

    return acc


def p3():
    grid, inverse, unique = parse_grid(3)

    exp_grid = {vmul(k, (2,2)):v for k,v in grid.items() if v == '#'}

    to_add = {}
    for point in exp_grid:
        for i, d in enumerate(DIRS):
            p = vadd(vmul(d, (2,2)), point)
            if p in exp_grid and exp_grid[p] == '#':
                to_add[vadd(point, d)] = '#'

    exp_grid |= to_add

    start, end = min(exp_grid), max(exp_grid)
    start = vsub(start, (1,1))
    end = vadd(end, (1,1))

    acc = 0
    min_dist = INF

    r_hand_map = {0: (1,1), 1: (1,-1), 2: (-1,-1), 3:(-1,1)}
    dir_map = {0:'>', 1:'^', 2:'<', 3:'v'}

    turtle = start
    tgt = end
    turtle_d = 0
    while True:
        r_hand_pos = vadd(turtle, r_hand_map[turtle_d])
        if vadd(turtle, DIRS[turtle_d]) in exp_grid:
            turtle_d = (turtle_d + 1) % 4
        elif r_hand_pos in exp_grid:
            turtle = vadd(turtle, vmul((2,2), DIRS[turtle_d]))
            acc += 1
        else:
            turtle_d = (turtle_d - 1) % 4

        if verbose:
            print_2d('  ', exp_grid, {start: 'S', end: 'E', turtle: dir_map[turtle_d]})

        if turtle == tgt:
            if tgt == end:
                min_dist, acc = min(min_dist, acc), 0
                tgt = start
            else:
                return min(min_dist, acc)


if __name__ == '__main__':
    setquest(17)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
