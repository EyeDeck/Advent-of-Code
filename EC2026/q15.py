from ec import *

def p1():
    grid, inverse, unique = parse_grid(1)

    src = (unique['S'], 0, frozenset())
    tgt = (unique['E'], 0, frozenset(inverse['@']))

    def get_neighbors(pos):
        neighbors = []
        for d_i, d_v in enumerate(DIRS):
            if d_i == (pos[1]-2) % 4:
                continue
            n = vadd(pos[0], d_v)
            if n not in grid:
                continue
            if grid[n] == '#':
                continue
            elif grid[n] == '@':
                neighbors.append(((n, d_i, frozenset({*pos[2], n})), 1))
            elif grid[n] in '.E':
                neighbors.append(((n, d_i, pos[2]), 1))
        return neighbors

    path = wbfs(src, tgt, get_neighbors)
    return len(path) - 1


def p2():
    grid, inverse, unique = parse_grid(2)

    src = (unique['S'], 0, 0)
    tgt = (unique['E'], 0, EqOp('>=', 2026))  # a touch of whimsy

    def get_neighbors(pos):
        neighbors = []
        for d_i, d_v in enumerate(DIRS):
            if d_i == (pos[1]-2) % 4:
                continue
            n = vadd(pos[0], d_v)
            if n not in grid:
                continue
            if grid[n] == '#':
                continue
            elif grid[n] == '@':
                neighbors.append(((n, d_i, pos[2]+1), 1))
            elif grid[n] in '.E':
                neighbors.append(((n, d_i, pos[2]), 1))
        return neighbors

    path = wbfs(src, tgt, get_neighbors)
    if verbose:
        print_2d(' ', grid, {pos[0]:'~' for pos in path})
    return len(path) - 1


def p3():
    grid, inverse, unique = parse_grid(3)

    why = 202620262026

    src = unique['S']
    tgt = unique['E']

    loop_point_list = []

    for start_x in range(src[0], tgt[0]):
        start_point = (start_x, src[1])
        pos, dir = start_point, 1
        pos = vadd(pos, DIRS[dir])
        if grid[pos] == '#':
            continue
        sec = 1
        sulphur = 0
        while pos != start_point:
            sec += 1
            if grid[pos] == '@':
                sulphur += 1
            next_pos = vadd(pos, DIRS[dir])
            if grid[next_pos] == '#':
                for d_i, d_v in enumerate(DIRS):
                    if d_i == (dir - 2) % 4:
                        continue
                    next_pos = vadd(pos, d_v)
                    if grid[next_pos] != '#':
                        pos = next_pos
                        dir = d_i
                        break
            else:
                pos = next_pos
        loop_point_list.append((start_point, sec, sulphur))

    loop_point_list.sort(key=lambda x: x[2]/x[1], reverse=True)

    def get_neighbors(pos):
        neighbors = []
        for d_i, d_v in enumerate(DIRS):
            if d_i == (pos[1]-2) % 4:
                continue
            n = vadd(pos[0], d_v)
            if n not in grid:
                continue
            if grid[n] == '#':
                continue
            elif grid[n] == '@':
                if n == best_loop[0]:
                    neighbors.append(((n, d_i, pos[2]+1, True), 1))
                else:
                    neighbors.append(((n, d_i, pos[2]+1, pos[3]), 1))
            elif grid[n] in '.E':
                if n == best_loop[0]:
                    neighbors.append(((n, d_i, pos[2], True), 1))
                else:
                    neighbors.append(((n, d_i, pos[2], pos[3]), 1))
        return neighbors

    best_loop = loop_point_list[0]
    fudge_factor = (why-300) // best_loop[2]
    sulphur_fudge = fudge_factor * best_loop[2]
    time_fudge = fudge_factor * best_loop[1]
    if verbose:
        print('fudge factor:', fudge_factor, 'sulphur_fudge', sulphur_fudge, 'time_fudge', time_fudge, 's_tgt', why - sulphur_fudge)

    path = wbfs((src, 0, 0, False), (tgt, 0, why - sulphur_fudge, True), get_neighbors)

    if verbose:
        print_2d(' ', grid, {k[0]:'~' for k in path})

    return len(path) + time_fudge - 1


if __name__ == '__main__':
    setquest(15)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
