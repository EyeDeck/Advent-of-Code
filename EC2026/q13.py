import itertools

from ec import *


# what a mess
def collides(a_start, b_start, a_end, b_end, units):
    half = units // 2

    a_delta = (a_end - a_start + half) % units - half
    b_delta = (b_end - b_start + half) % units - half

    start_diff = a_start - b_start
    end_diff = start_diff + a_delta - b_delta

    low, high = sorted((start_diff, end_diff))
    first = -((-low) // units)
    last = high // units

    if first > last:
        return False

    if start_diff % units == 0:
        start_multiple = start_diff // units
        return first < start_multiple or last > start_multiple

    return True


def solve(data):
    data = {k: [int(s) if s.isnumeric() else s for s in v.split(':')] for k, v in [line.split(' ') for line in data]}

    data['direction'] = [1 if d == 'CW' else -1 for d in data['direction']]

    hand_ct = len(data['hands'])

    if verbose:
        print('processing', data)

    acc = 0
    for hand_index_a, hand_index_b in itertools.combinations(range(hand_ct), 2):
        temp_acc = 0

        tick_until = 0

        a_ticks, b_ticks = data['hands'][hand_index_a], data['hands'][hand_index_b]
        a_dir, b_dir = data['direction'][hand_index_a], data['direction'][hand_index_b]
        a_pos, b_pos = [data['current'][hand_index_a], data['current'][hand_index_b]]
        a_moves, b_moves = data['move'][hand_index_a], data['move'][hand_index_b]

        max_seconds = max(a_moves, b_moves)
        min_seconds = min(a_moves, b_moves)

        pair_mult = a_ticks * b_ticks

        a_pos *= b_ticks
        b_pos *= a_ticks

        a_vel = b_ticks * a_dir
        b_vel = a_ticks * b_dir

        if verbose:
            print(
                f'starting hand pair with tick counts {a_ticks}, {b_ticks} | dirs {a_dir}, {b_dir} | start pos {a_pos}, {b_pos} | tick length {a_moves}, {b_moves}')

        second = 0
        loop_tgt, loop_start = (a_pos, b_pos), 0
        while second < max_seconds:
            second += 1

            a_start, b_start = a_pos, b_pos
            if second <= a_moves:
                a_pos += a_vel
                a_pos %= pair_mult
            if second <= b_moves:
                b_pos += b_vel
                b_pos %= pair_mult

            collides_this_turn = collides(a_start, b_start, a_pos, b_pos, pair_mult)
            if collides_this_turn:
                temp_acc += 1

            if (
                    (tick_until != 0 and second >= tick_until) or
                    (tick_until == 0 and second == min_seconds and min_seconds > 0)
            ):
                tick_until = 0
                loop_tgt = (a_pos, b_pos)
                loop_start = second
                acc += temp_acc
                if verbose:
                    print('limit reached; one hand stopped')
                    print('cleared loop_start and committed temp_acc which was', temp_acc)
                    print('now we should tick until another cycle')
                temp_acc = 0

            elif loop_tgt == (a_pos, b_pos):
                tick_until = min_seconds if second < min_seconds else max_seconds

                len_of_cycle = second - loop_start
                cycles_to_skip = (tick_until - second) // len_of_cycle
                second_to_skip_to = second + len_of_cycle * cycles_to_skip
                if verbose:
                    print('returned to start at second', second, 'meaning len of cycle is', len_of_cycle)
                    print('so we should skip', cycles_to_skip, 'cycles to end up at second', second_to_skip_to)
                    print('each cycle counted', temp_acc, 'collisions, so add', temp_acc * (cycles_to_skip + 1),
                          'collisions')
                    print('now tick normally until cycle', tick_until, '...')

                temp_acc *= cycles_to_skip + 1
                if verbose:
                    print('temp_acc:', temp_acc)
                second = second_to_skip_to

        if verbose:
            print('hand pair', hand_index_a, hand_index_b, 'remainder:', temp_acc)
        acc += temp_acc

    if verbose:
        print('meetings', acc, '\n')
    return acc


if __name__ == '__main__':
    setquest(13)

    print('part1:', solve(parse_lines(1)))
    print('part2:', sum(solve(line.split('\n')) for line in parse_double_break(2)))
    print('part3:', sum(solve(line.split('\n')) for line in parse_double_break(3)))
