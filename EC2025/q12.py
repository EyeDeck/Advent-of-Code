from ec import *


def do_adj(grid, start):
    q = [start]
    seen = {*q}
    while q:
        cur = q.pop()
        v = grid[cur]
        for d in DIRS:
            n = vadd(cur, d)
            if n not in grid or n in seen:
                continue
            n_v = grid[n]
            if n_v <= v:
                q.append(n)
                seen.add(n)
    return seen


def p1():
    grid, inverse, unique = parse_grid(1)
    return len(do_adj(grid, (0, 0)))


def p2():
    grid, inverse, unique = parse_grid(2)
    bounds = grid_bounds(grid)
    t_l = do_adj(grid, (0, 0))
    b_r = do_adj(grid, (bounds[2:]))
    return len(t_l | b_r)


def p3():
    grid, inverse, unique = parse_grid(3)

    acc = 0
    for loop in range(3):
        points_to_bother_testing = set(grid.keys())
        best_ct = 0
        best_r = None
        i = 0
        while points_to_bother_testing:
            i += 1
            if i % 20 == 0:
                print(f'{loop + 1}/3, {len(points_to_bother_testing)}   ', end='\r')
            point = points_to_bother_testing.pop()
            r = do_adj(grid, point)
            ct = len(r)
            if ct > best_ct:
                best_ct = ct
                best_r = r
            # any point part of a previous test is necessarily a subset of that previous test, so skip all of them
            points_to_bother_testing -= r
        grid = {k: v for k, v in grid.items() if k not in best_r}
        acc += best_ct

    return acc


setquest(12)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
