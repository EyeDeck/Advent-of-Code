from ec import *


def gen_neighbors(grid, width=0):
    all_neighbors = {}
    for pos in grid:
        neighbors = []

        if width:
            r_pos = rotate(pos, width)
        else:
            r_pos = pos

        if (r_pos[0] + r_pos[1]) & 1:
            dirs = [(-1, 0), (1, 0), (0, 1)]
        else:
            dirs = [(-1, 0), (1, 0), (0, -1)]

        if width:
            dirs.append((0, 0))

        for offset in dirs:
            n_pos = vadd(r_pos, offset)
            if n_pos in grid and grid[n_pos] in {'T', 'S', 'E'}:
                neighbors.append(n_pos)

        all_neighbors[pos] = neighbors
    return all_neighbors


def p1():
    grid, inverse, unique = parse_grid(1)
    grid = {k:v for k,v in grid.items() if v=='T'}

    neighbors = gen_neighbors(grid)

    acc = 0
    for n in neighbors.values():
        acc += len(n)

    return acc // 2


def p2():
    grid, inverse, unique = parse_grid(2)

    neighbors = gen_neighbors(grid)

    path = bfs(unique['S'], unique['E'], neighbors)

    if verbose:
        print_2d('.', grid, {k: '@' for k in path})

    return len(path) - 1


def rotate(pos, width):
    # jesus christ
    x, y = pos
    y_r = (width - x - y) // 2
    x_r = y_r + y * 2 + (x - y) % 2
    return x_r, y_r


def p3():
    grid, inverse, unique = parse_grid(3)

    bounds = grid_bounds(grid)
    width, height = bounds[2:]

    neighbors = gen_neighbors(grid, width)

    path = bfs(unique['S'], unique['E'], neighbors)

    if verbose:
        print_2d('.', grid, {k: '@' for k in path})

    return len(path) - 1


setquest(20)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
