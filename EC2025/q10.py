from ec import *


def p1():
    grid, inverse, unique = parse_grid(1)
    depth = 4

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
            for pos in (vadd(cur_pos, off) for off in dragon_moves):
                next_state = (pos, cur_depth + 1)
                if next_state in seen_states:
                    continue
                seen_states.add(next_state)
                q.append(next_state)
    return acc


def p2():
    grid, inverse, unique = parse_grid(2)
    max_depth = 20

    dragon = unique['D']
    sheep = inverse['S']
    hideouts = inverse['#']

    # calculate each set of all reachable tiles for the dragon, indexed per turn
    dragon_reachable = [set() for _ in range(max_depth)]
    q = [(dragon, 0)]
    while q:
        dragon_pos, depth = q.pop()

        if depth < max_depth:
            for dragon_ticked in (vadd(dragon_pos, off) for off in dragon_moves):
                if dragon_ticked not in dragon_reachable[depth]:
                    dragon_reachable[depth].add(dragon_ticked)
                    q.append((dragon_ticked, depth + 1))

    # tick all the sheep and find out if they overlap with a dragon on either the start or end of their turn
    acc = 0
    for dragon_positions in dragon_reachable:
        next_sheep = set()
        for sheep_start in sheep:
            if sheep_start in dragon_positions and sheep_start not in hideouts:
                acc += 1
                continue
            sheep_end = vadd((0, 1), sheep_start)
            if sheep_end in dragon_positions and sheep_end not in hideouts:
                acc += 1
            else:
                next_sheep.add(sheep_end)

        sheep = next_sheep

    return acc


def p3():
    grid, inverse, unique = parse_grid(3)
    dragon = unique['D']
    sheep = inverse['S']
    hideouts = inverse['#']

    # pre-cache valid adjacent tiles for each dragon location
    dragon_legal_moves = {pos: [c for move in dragon_moves if (c := vadd(pos, move)) in grid] for pos in grid}

    # save some computation by ending the search early if a sheep hits an unbroken chain of hideouts to the exit
    bounds = grid_bounds(grid)
    sheep_goals = {x: bounds[3] + 1 for x in range(bounds[2] + 1)}
    for x in range(bounds[0], bounds[2] + 1):
        for y in range(bounds[1], bounds[3] + 1):
            if all(grid[x, y2] == '#' for y2 in range(y, bounds[3] + 1)):
                sheep_goals[x] = y
                break
    # also pre-cache sheep moves, while we're at it (it's a surprising speedup)
    sheep_moves = {(x, y): (-1 if sheep_goals[x] == y + 1 else (x, y + 1)) for (x, y) in grid}

    @memo
    def get_win_count(dragon_pos, sheep_all, turn):
        if not sheep_all:
            return 1
        acc = 0

        if turn:  # sheep
            has_sheep_moved = False
            for i, sheep in enumerate(sheep_all):
                sheep_ticked = sheep_moves[sheep]
                if sheep_ticked == -1:
                    # sheep had a valid move and won, do not let dragon move twice in a row
                    has_sheep_moved = True
                    continue
                if sheep_ticked == dragon_pos and dragon_pos not in hideouts:
                    # sheep trying to move into dragon, skip this move
                    continue

                sheep_all_next = list(sheep_all)
                sheep_all_next[i] = sheep_ticked
                sheep_all_next = tuple(sheep_all_next)

                has_sheep_moved = True

                acc += get_win_count(dragon_pos, sheep_all_next, False)

            if not has_sheep_moved:
                # skip sheep's turn if no sheep was able to move
                acc += get_win_count(dragon_pos, sheep_all, False)

        else:  # dragon
            for dragon_ticked in dragon_legal_moves[dragon_pos]:
                sheep_all_next = sheep_all

                if dragon_ticked in sheep_all and dragon_ticked not in hideouts:
                    sheep_all_next = list(sheep_all_next)
                    sheep_all_next.remove(dragon_ticked)
                    sheep_all_next = tuple(sheep_all_next)

                acc += get_win_count(dragon_ticked, sheep_all_next, True)
        return acc

    return get_win_count(dragon, tuple(sorted(sheep)), True)



setquest(10)

dragon_moves = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
