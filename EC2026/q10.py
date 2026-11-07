import copy
from ec import *

DIR_MAP = {
    '>': [(1,0), 'v'],
    'v': [(0,1), '<'],
    '<': [(-1,0), '^'],
    '^': [(0,-1), '>'],

}


def p1():
    grid, inverse, unique = parse_grid(1)
    nullghosts_pos = set(inverse['>'] + inverse['<'] + inverse['^'] + inverse['v'])

    board = set(inverse['.']) | nullghosts_pos

    nullghosts = defaultdict(dict)
    for ng_id, ng_pos in enumerate(nullghosts_pos):
        nullghosts[ng_id]['pos'] = ng_pos
        nullghosts[ng_id]['dir'] = grid[ng_pos]
        nullghosts[ng_id]['collisions'] = 0

    print(nullghosts)

    total_collisions = 0

    for round in range(1,11):
        nullghosts_pos = defaultdict(int)
        new_collisions = 0
        for ng_id, ng in nullghosts.items():
            nxt = vadd(DIR_MAP[ng['dir']][0], ng['pos'])
            if nxt in board:
                nullghosts_pos[nxt] += 1
                ng['pos'] = nxt
            else:
                nullghosts_pos[ng['pos']] += 1
                ng['collisions'] += 1
                new_collisions += 1
                ng['dir'] = DIR_MAP[ng['dir']][1]

        for ng_id, ng in nullghosts.items():
            if nullghosts_pos[ng['pos']] > 1:
                ng['dir'] = DIR_MAP[DIR_MAP[ng['dir']][1]][1]
                ng['collisions'] += 1
                new_collisions += 1
        total_collisions += new_collisions
        print(f'Round: {round}\nCollisions: {new_collisions}')
        print_2d(
            '  ',
             {k:'.' for k in board},
             {ng['pos']:ng['dir'] for ng in nullghosts.values()},
             {k:v for k,v in nullghosts_pos.items() if v > 1},
             {k:'#' for k in inverse['#']}
        )

    return total_collisions


def p2():
    grid, inverse, unique = parse_grid(2)
    nullghosts_pos = set(inverse['>'] + inverse['<'] + inverse['^'] + inverse['v'])

    board = set(inverse['.']) | nullghosts_pos

    nullghosts = defaultdict(dict)
    for ng_id, ng_pos in enumerate(nullghosts_pos):
        nullghosts[ng_id]['pos'] = ng_pos
        nullghosts[ng_id]['dir'] = grid[ng_pos]
        nullghosts[ng_id]['collisions'] = 0

    print(nullghosts)

    total_collisions = 0

    for round in range(1, 100_000_000):
        nullghosts_pos = defaultdict(int)
        dead_ghosts = []
        new_collisions = 0
        for ng_id, ng in nullghosts.items():
            nxt = vadd(DIR_MAP[ng['dir']][0], ng['pos'])
            if nxt in board:
                nullghosts_pos[nxt] += 1
                ng['pos'] = nxt
            else:
                nullghosts_pos[ng['pos']] += 1
                ng['collisions'] += 1
                if ng['collisions'] >= 10_000:
                    dead_ghosts.append(ng_id)
                new_collisions += 1
                ng['dir'] = DIR_MAP[ng['dir']][1]

        for ng in dead_ghosts:
            nullghosts.pop(ng)

        dead_ghosts = []
        for ng_id, ng in nullghosts.items():
            if nullghosts_pos[ng['pos']] > 1:
                ng['dir'] = DIR_MAP[DIR_MAP[ng['dir']][1]][1]
                ng['collisions'] += 1
                new_collisions += 1
                if ng['collisions'] >= 10_000:
                    dead_ghosts.append(ng_id)

        for ng in dead_ghosts:
            nullghosts.pop(ng)

        total_collisions += new_collisions
        if verbose:
            print(f'Round: {round}\nCollisions: {new_collisions}')
            print_2d(
                '  ',
                {k: '.' for k in board},
                {ng['pos']: ng['dir'] for ng in nullghosts.values()},
                {k: v for k, v in nullghosts_pos.items() if v > 1},
                {k: '#' for k in inverse['#']}
            )

        if len(nullghosts) == 0:
            return round

    return None


def p3():
    grid, inverse, unique = parse_grid(3)
    nullghosts_pos = set(inverse['>'] + inverse['<'] + inverse['^'] + inverse['v'])

    board = set(inverse['.']) | nullghosts_pos

    nullghosts = defaultdict(dict)
    for ng_id, ng_pos in enumerate(nullghosts_pos):
        nullghosts[ng_id]['pos'] = ng_pos
        nullghosts[ng_id]['dir'] = grid[ng_pos]
        nullghosts[ng_id]['collisions'] = 0

    print(nullghosts)

    total_collisions = 0

    hashable_states = {}
    previous_state = None

    round = 0
    while True:
        round += 1

        nullghosts_pos = defaultdict(int)
        dead_ghosts = []
        new_collisions = 0
        for ng_id, ng in nullghosts.items():
            nxt = vadd(DIR_MAP[ng['dir']][0], ng['pos'])
            if nxt in board:
                nullghosts_pos[nxt] += 1
                ng['pos'] = nxt
            else:
                nullghosts_pos[ng['pos']] += 1
                ng['collisions'] += 1
                if ng['collisions'] >= 1000000000000:
                    dead_ghosts.append(ng_id)
                new_collisions += 1
                ng['dir'] = DIR_MAP[ng['dir']][1]

        if dead_ghosts:
            for ng in dead_ghosts:
                nullghosts.pop(ng)
            print(f'Round: {round}   {len(nullghosts)} | Dead ghosts: {dead_ghosts}')

        dead_ghosts = []
        for ng_id, ng in nullghosts.items():
            if nullghosts_pos[ng['pos']] > 1:
                ng['dir'] = DIR_MAP[DIR_MAP[ng['dir']][1]][1]
                ng['collisions'] += 1
                new_collisions += 1
                if ng['collisions'] >= 1000000000000:
                    dead_ghosts.append(ng_id)

        if dead_ghosts:
            for ng in dead_ghosts:
                nullghosts.pop(ng)
            print(f'Round: {round}   {len(nullghosts)} | Dead ghosts: {dead_ghosts}')

        total_collisions += new_collisions
        if verbose:
            print(f'Round: {round}\nCollisions: {new_collisions}')
            print_2d(
                '  ',
                {k: '.' for k in board},
                {ng['pos']: ng['dir'] for ng in nullghosts.values()},
                {k: v for k, v in nullghosts_pos.items() if v > 1},
                {k: '#' for k in inverse['#']}
            )

        # if round % 1_000_000 == 0:
        #     max_coll = max(nullghosts.values(), key=lambda x: x['collisions'])['collisions']
        #     print(f'Round: {round} (max collision ct: {max_coll / 1000000000000 * 100}%)')

        state = tuple(tuple((ng_id, ng['pos'], ng['dir'])) for ng_id, ng in nullghosts.items())
        if state in hashable_states:

            cycle_start_round, cycle_start_state = hashable_states[state]

            hashable_states = {}

            cycle_len = round - cycle_start_round
            print(f'cycle detected from {cycle_start_round} to {round} ({cycle_len} rounds)')
            diffs = {k:nullghosts[k]['collisions']-cycle_start_state[k]['collisions'] for k,v in nullghosts.items()}
            print(diffs)

            min_req_to_kill_ghost = INF
            for k,v in diffs.items():
                cycles_to_kill_ghost = ((1000000000000-1) - cycle_start_state[k]['collisions']) // v - 1
                min_req_to_kill_ghost = min(min_req_to_kill_ghost, cycles_to_kill_ghost)

            round = min_req_to_kill_ghost * cycle_len + round

            print('minreq', min_req_to_kill_ghost, 'next round', round)

            for k,v in diffs.items():
                nullghosts[k]['collisions'] += v * min_req_to_kill_ghost

            print('ng after correction:', nullghosts, 'set to round', round)

            dead_ghosts = []
            for ng_id, ng in nullghosts.items():
                if ng['collisions'] >= 1000000000000:
                    dead_ghosts.append(ng_id)

            if dead_ghosts:
                for ng in dead_ghosts:
                    nullghosts.pop(ng)
                print(f'Round: {round}   {len(nullghosts)} | Dead ghosts: {dead_ghosts}')

            print('ng:', nullghosts)

        state_copy = copy.deepcopy(nullghosts)
        hashable_states[state] = [round, state_copy]

        previous_state = state_copy

        if len(nullghosts) == 0:
            return round


if __name__ == '__main__':
    setquest(10)

    # print('part1:', p1())
    # print('part2:', p2())
    print('part3:', p3())
