import copy
from ec import *

DIR_MAP = {
    '>': [(1,0), 'v'],
    'v': [(0,1), '<'],
    '<': [(-1,0), '^'],
    '^': [(0,-1), '>'],

}


def solve(part, ghost_health):
    grid, inverse, unique = parse_grid(part)
    nullghosts_pos = set(inverse['>'] + inverse['<'] + inverse['^'] + inverse['v'])

    board = set(inverse['.']) | nullghosts_pos

    nullghosts = defaultdict(dict)
    for ng_id, ng_pos in enumerate(nullghosts_pos):
        nullghosts[ng_id]['pos'] = ng_pos
        nullghosts[ng_id]['dir'] = grid[ng_pos]
        nullghosts[ng_id]['collisions'] = 0

    total_collisions = 0

    hashable_states = {}

    round_ct = 0
    while True:
        round_ct += 1

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
                if ng['collisions'] >= ghost_health:
                    dead_ghosts.append(ng_id)
                new_collisions += 1
                ng['dir'] = DIR_MAP[ng['dir']][1]

        if dead_ghosts:
            for ng in dead_ghosts:
                nullghosts.pop(ng)
            if verbose:
                print(f'Round: {round_ct}   {len(nullghosts)} | Dead ghosts (wall collision): {dead_ghosts}')

        dead_ghosts = []
        for ng_id, ng in nullghosts.items():
            if nullghosts_pos[ng['pos']] > 1:
                ng['dir'] = DIR_MAP[DIR_MAP[ng['dir']][1]][1]
                ng['collisions'] += 1
                new_collisions += 1
                if ng['collisions'] >= ghost_health:
                    dead_ghosts.append(ng_id)

        if dead_ghosts:
            for ng in dead_ghosts:
                nullghosts.pop(ng)
            if verbose:
                print(f'Round: {round_ct}   {len(nullghosts)} | Dead ghosts (ghost collision): {dead_ghosts}')

        total_collisions += new_collisions
        if verbose and do_step:
            print(f'Round: {round_ct}\nCollisions: {new_collisions}')
            print_2d(
                '  ',
                {k: '.' for k in board},
                {ng['pos']: ng['dir'] for ng in nullghosts.values()},
                {k: v for k, v in nullghosts_pos.items() if v > 1},
                {k: '#' for k in inverse['#']}
            )
            input()

        state = tuple(tuple((ng_id, ng['pos'], ng['dir'])) for ng_id, ng in nullghosts.items())

        if state in hashable_states:
            cycle_start_round, cycle_start_state = hashable_states[state]

            hashable_states = {}

            cycle_len = round_ct - cycle_start_round
            if verbose:
                print(f'cycle detected from {cycle_start_round} to {round_ct} ({cycle_len} rounds)')
            diffs = {k:nullghosts[k]['collisions']-cycle_start_state[k]['collisions'] for k,v in nullghosts.items()}

            min_req_to_kill_ghost = INF
            for k,v in diffs.items():
                cycles_to_kill_ghost = ((ghost_health-1) - cycle_start_state[k]['collisions']) // v - 1
                min_req_to_kill_ghost = min(min_req_to_kill_ghost, cycles_to_kill_ghost)

            round_ct = min_req_to_kill_ghost * cycle_len + round_ct

            if verbose:
                print('minreq', min_req_to_kill_ghost, 'next round_ct', round_ct)

            for k,v in diffs.items():
                nullghosts[k]['collisions'] += v * min_req_to_kill_ghost

        state_copy = copy.deepcopy(nullghosts)
        hashable_states[state] = [round_ct, state_copy]

        if part == 1 and round_ct == 10:
            return total_collisions
        if len(nullghosts) == 0:
            return round_ct


if __name__ == '__main__':
    setquest(10)

    do_step = '-s' in sys.argv or '--step' in sys.argv

    print('part1:', solve(1, INF))
    print('part2:', solve(2, 10000))
    print('part3:', solve(3, 1000000000000))
