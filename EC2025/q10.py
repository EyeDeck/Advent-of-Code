from ec import *


def p1():
    grid, inverse, unique = parse_grid(1)
    depth = 4

    # print(grid)

    q = [(unique['D'], 0)]

    acc = 0
    seen_states = set()
    seen_pos = set()
    while q:
        cur = q.pop()
        cur_pos, cur_depth = cur

        if grid[cur_pos] == 'S' and cur_pos not in seen_pos:
            acc += 1
            seen_pos.add(cur_pos)

        if cur_depth < depth:
            for pos in (vadd(cur_pos, off) for off in
                        [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]):
                next_state = (pos, cur_depth + 1)
                if next_state in seen_states:
                    continue
                seen_states.add(next_state)
                q.append(next_state)
    return acc


def p2():
    grid, inverse, unique = parse_grid(2)
    max_depth = 20

    dragon_pos = unique['D']
    hideouts = inverse['#']
    all_sheep = inverse['S']

    # print(all_sheep)
    # print('hideouts:')
    # print(hideouts)

    possible_dragon_positions = defaultdict(set)
    q = [(dragon_pos, 0)]
    while q:
        cur_pos, cur_depth = q.pop()

        if cur_depth < max_depth:
            next_depth = cur_depth + 1
            for next_pos in (vadd(cur_pos, off) for off in dragon_moves):
                if next_pos not in possible_dragon_positions[next_depth]:
                    q.append((next_pos, next_depth))
                    possible_dragon_positions[next_depth].add(next_pos)
        # print('poss', possible_dragon_positions)

    # print(possible_dragon_positions)

    acc = 0
    for i in range(1, max_depth + 1):
        dead_sheep = set()
        next_sheep = set()
        for sheep in all_sheep:
            if sheep in possible_dragon_positions[i] and sheep not in hideouts:
                dead_sheep.add(sheep)
                acc += 1
                continue
            next_pos = vadd((0, 1), sheep)
            if next_pos in possible_dragon_positions[i] and next_pos not in hideouts:
                dead_sheep.add(next_pos)
                acc += 1
            else:
                next_sheep.add(next_pos)
        # print_2d('. ', {k:'D' for k in possible_dragon_positions[i] if k not in hideouts}, {k:'S' for k in all_sheep}, {k:'#' for k in hideouts}, {k:'X' for k in dead_sheep} )

        all_sheep = next_sheep

    return acc


def p3():
    grid, inverse, unique = parse_grid(3)
    dragon_pos = unique['D']
    hideouts = inverse['#']
    all_sheep = inverse['S']

    bounds = grid_bounds(grid)
    print(bounds)
    sheep_goals = {x: bounds[3] + 1 for x in range(bounds[2]+1)}
    print(sheep_goals)
    for x in range(bounds[0], bounds[2]+1):
        for y in range(bounds[1], bounds[3]+1):
            print(x, y, [grid[x, y2] == '#' for y2 in range(y, bounds[3]+1)])
            if all(grid[x, y2] == '#' for y2 in range(y, bounds[3]+1)):
                sheep_goals[x] = y
                break
    print(sheep_goals)
    sheep_goals = {(k,v) for k,v in sheep_goals.items()}

    # return

    @memo
    def get_win_count(dragon, sheep, turn):
        # print('running', dragon, sheep, turn)
        # print_2d('. ', {c:'.' for c in all_sheep}, {c:'#' for c in hideouts}, {dragon:'D'}, {c:'S' for c in sheep})
        # input()
        if len(sheep) == 0:
            # print('returned 1')
            return 1
        acc = 0

        if turn:  # sheep
            has_sheep_moved = False
            for sh in sheep:
                ticked_sheep = vadd(sh, (0, 1))
                if ticked_sheep in sheep_goals:
                    has_sheep_moved = True
                    # print(f'sheep {sh} moving down would win--skipping')
                    continue
                if ticked_sheep == dragon and dragon not in hideouts:
                    continue

                next_sheep = sheep - {sh} | {ticked_sheep}
                has_sheep_moved = True

                acc += get_win_count(dragon, next_sheep, False)

            if not has_sheep_moved:
                # print('no sheep could move:', sheep, dragon)
                acc += get_win_count(dragon, sheep, False)
        else:
            for ticked_dragon in (vadd(dragon, off) for off in dragon_moves):
                next_sheep = sheep
                if ticked_dragon not in grid:
                    continue
                if ticked_dragon in next_sheep and ticked_dragon not in hideouts:
                    # print(f'dragon ate {ticked_dragon}')
                    next_sheep = next_sheep - {ticked_dragon}

                acc += get_win_count(ticked_dragon, next_sheep, True)

        # print('returned', acc)
        return acc

    return get_win_count(dragon_pos, frozenset(all_sheep), True)


setquest(10)

dragon_moves = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
