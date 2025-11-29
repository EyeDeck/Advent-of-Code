from ec import *


def p1():
    grid, inverse, unique = parse_grid(1)

    dirs = [(-1, 0), (1, 0), (0, -1)]
    acc = 0
    for pos in grid:
        if grid[pos] != 'T':
            continue
        for o in dirs:
            other_pos = vadd(pos, o)
            if other_pos in grid and grid[other_pos] == 'T':
                acc += 1

    return acc // 2


def p2():
    grid, inverse, unique = parse_grid(2)

    def get_neighbors(pos):
        neighbors = []
        if (pos[0] + pos[1]) & 1:
            dirs = [(-1, 0), (1, 0), (0, 1)]
        else:
            dirs = [(-1, 0), (1, 0), (0, -1)]
        for o in dirs:
            other_pos = vadd(pos, o)
            if other_pos in grid and grid[other_pos] in {'T', 'S', 'E'}:
                print(grid[other_pos])
                neighbors.append((other_pos, 1))
        print(pos, neighbors)
        return neighbors

    print(unique['S'], unique['E'])
    path = wbfs(unique['S'], unique['E'], get_neighbors)
    print(path)

    print_2d('.', grid, {k: '@' for k in path})

    return len(path) - 1


def p3():
    grid, inverse, unique = parse_grid(3)

    def get_neighbors(pos):
        print('started at', pos)
        pos = rotate(pos)
        print('rotated to', pos)
        neighbors = []
        if (pos[0] + pos[1]) & 1:
            print('which is an up triangle')
            dirs = [(0, 0), (-1, 0), (1, 0), (0, 1)]
        else:
            print('which is a down triangle')
            dirs = [(0, 0), (-1, 0), (1, 0), (0, -1)]
        for o in dirs:
            other_pos = vadd(pos, o)
            print('checking coord', other_pos)
            if other_pos in grid and grid[other_pos] in {'T', 'S', 'E'}:
                print(grid[other_pos])
                neighbors.append((other_pos, 1))
        print('and has neighbors', neighbors)
        return neighbors

    bounds = grid_bounds(grid)
    width, height = bounds[2:]

    def rotate(pos):
        # jesus christ
        x, y = pos
        y_r = (width - x - y) // 2
        x_r = y_r + y * 2 + (x - y) % 2
        return x_r, y_r

    rotated_grid = {}
    for pos, v in grid.items():
        if v == '.':
            continue
        rotated_grid[rotate(pos)] = v
    # print_2d('.', grid, {pos:'A', r_pos:'B'})
    print_2d('.', rotated_grid)

    rotated_grid2 = {}
    for pos, v in rotated_grid.items():
        if v == '.':
            continue
        rotated_grid2[rotate(pos)] = v
    # print_2d('.', grid, {pos:'A', r_pos:'B'})
    print_2d('.', rotated_grid2)

    print(unique['S'], unique['E'])
    path = wbfs(unique['S'], unique['E'], get_neighbors)
    print(path)

    print_2d('.', grid, {k: '@' for k in path})

    return len(path) - 1


setquest(20)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
