import itertools
import math

from ec import *


def p1():
    data = parse_lines(1)
    data = {k:[int(s) if s.isnumeric() else s for s in v.split(':')] for k,v in [line.split(' ') for line in data]}

    print(data)

    hand_ct = len(data['hands'])

    acc = 0

    for hand_i_a, hand_i_b in itertools.combinations(range(hand_ct), 2):
        positions = data['hands'][hand_i_a], data['hands'][hand_i_b]
        directions = data['direction'][hand_i_a], data['direction'][hand_i_b]
        currents = [data['current'][hand_i_a], data['current'][hand_i_b]]
        moves = data['move'][hand_i_a], data['move'][hand_i_b]
        print(positions, directions, currents, moves)

        discrete_positions = math.prod(positions)
        # currents = [i * discrete_positions for i in currents]
        currents = [currents[0] * positions[1], currents[1] * positions[0]]

        total_seconds = max(moves)
        # position_data = [[0]*(discrete_positions * total_seconds)]*2

        print(positions, directions, currents, moves)
        print(discrete_positions, currents, total_seconds)
        # print(position_data)

        a_dir, b_dir = [1 if d == 'CW' else -1 for d in directions]

        for second in range(total_seconds):
            s_pos = [[-1 for x in range(discrete_positions)] for y in range(2)]
            # print('s_pos', s_pos)
            for tick in range(positions[1]):
                # print('hand a', tick*positions[0])
                if second <= moves[0]:
                    currents[0] += a_dir
                    currents[0] %= discrete_positions
                s_pos[0][tick*positions[0]] = currents[0]
            for tick in range(positions[0]):
                # print('hand b', tick*positions[1])
                if second <= moves[1]:
                    currents[1] += b_dir
                    currents[1] %= discrete_positions
                s_pos[1][tick*positions[1]] = currents[1]

            last_a, last_b = 0, 0
            for i in range(discrete_positions):
                if s_pos[0][i] != -1:
                    last_a = s_pos[0][i]
                if s_pos[1][i] != -1:
                    last_b = s_pos[1][i]
                s_pos[0][i] = last_a
                s_pos[1][i] = last_b


            print(f'post:\n{s_pos[0]}\n{s_pos[1]}')

            if any(a==b for a,b in zip(s_pos[0], s_pos[1])):
                print(f'overlap on second {second} between hands {hand_i_a}, {hand_i_b}')
                acc += 1

    return acc

# it's 20-something lol (not 25, 27)
# okay this discretization idea is stupid and isn't going to work out


def p1():
    data = parse_lines(1)
    data = {k:[int(s) if s.isnumeric() else s for s in v.split(':')] for k,v in [line.split(' ') for line in data]}

    data['direction'] = [1 if d == 'CW' else -1 for d in data['direction']]

    print(data)

    hand_ct = len(data['hands'])

    acc = 0

    def collides(a_start, a_end, b_start, b_end):
        return (a_start - b_start) * (a_end - b_end) < 0 or a_end == b_end

    for hand_index_a, hand_index_b in itertools.combinations(range(hand_ct), 2):
        positions = data['hands'][hand_index_a], data['hands'][hand_index_b]
        directions = data['direction'][hand_index_a], data['direction'][hand_index_b]
        currents = [data['current'][hand_index_a], data['current'][hand_index_b]]
        moves = data['move'][hand_index_a], data['move'][hand_index_b]

        total_seconds = max(moves)
        currents = [currents[0] * positions[1], currents[1] * positions[0]]

        pair_mult = math.prod(positions)

        print(positions, directions, currents, moves, total_seconds, pair_mult)

        for second in range(1, total_seconds+1):
            a_start, b_start = currents
            a_start += pair_mult
            b_start += pair_mult
            a_end, b_end = a_start, b_start

            if second <= moves[0]:
                a_end += positions[1] * directions[0]
            if second <= moves[1]:
                b_end += positions[0] * directions[1]

            # a_end = a_end % pair_mult + pair_mult
            # b_end = b_end % pair_mult + pair_mult

            print(a_start, b_start, '->', a_end, b_end)
            if collides(a_start, a_end, b_start, b_end) or a_end % pair_mult == b_end % pair_mult:
                print(f'hands {hand_index_a+1}, {hand_index_b+1} collided at {second}s')
                acc += 1

            a_end %= pair_mult
            b_end %= pair_mult

            currents = [a_end, b_end]


    return acc


def p1():
    return solve_for(parse_lines(1))


def solve_for(data):
    data = {k:[int(s) if s.isnumeric() else s for s in v.split(':')] for k,v in [line.split(' ') for line in data]}

    data['direction'] = [1 if d == 'CW' else -1 for d in data['direction']]

    print(data)

    hand_ct = len(data['hands'])

    acc = 0

    # oh my god
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

    for hand_index_a, hand_index_b in itertools.combinations(range(hand_ct), 2):
        this_acc = 0

        a_ticks, b_ticks = data['hands'][hand_index_a], data['hands'][hand_index_b]
        a_dir, b_dir = data['direction'][hand_index_a], data['direction'][hand_index_b]
        a_pos, b_pos = [data['current'][hand_index_a], data['current'][hand_index_b]]
        a_moves, b_moves = data['move'][hand_index_a], data['move'][hand_index_b]

        max_seconds = max(a_moves, b_moves)

        pair_mult = a_ticks * b_ticks
        hour_mult = (12/pair_mult)

        a_pos *= b_ticks
        b_pos *= a_ticks

        a_vel = b_ticks * a_dir
        b_vel = a_ticks * b_dir

        # print(positions, directions, currents, moves, total_seconds, pair_mult)
        #
        # a_vel = positions[1] * directions[0]
        # b_vel = positions[0] * directions[1]
        #
        # if a_vel == b_vel:
        #     continue
        #
        # for second in range(1, total_seconds+1):
        #     t = ((currents[1] - currents[0]) % pair_mult) / (a_vel - b_vel)
        #     print(t)
        #     currents[0] = currents[0] + a_vel % pair_mult
        #     currents[1] = currents[1] + b_vel % pair_mult

        # print(f'{a_ticks}, {b_ticks} | {a_dir}, {b_dir} | {a_pos*hour_mult}, {b_pos*hour_mult} | {a_moves}, {b_moves}')
        print(f'{a_ticks}, {b_ticks} | {a_dir}, {b_dir} | {a_pos}, {b_pos} | {a_moves}, {b_moves}')
        # print(pair_mult, hour_mult)

        for second in range(1, max_seconds+1):
            a_start, b_start = a_pos, b_pos
            if second <= a_moves:
                a_pos += a_vel
                a_pos %= pair_mult
            if second <= b_moves:
                b_pos += b_vel
                b_pos %= pair_mult

            # collides_this_turn = collides(a_start*hour_mult, b_start*hour_mult, a_pos*hour_mult, b_pos*hour_mult, 12)
            collides_this_turn = collides(a_start, b_start, a_pos, b_pos, pair_mult)
            # print(a_pos, b_pos, collides_this_turn)
            if collides_this_turn:
                this_acc += 1
            # print(a_pos*hour_mult, b_pos*hour_mult, collides(a_start, b_start, a_pos, b_pos, pair_mult))
        print('acc:', this_acc)
        acc += this_acc

    print(acc)
    return acc


def p2():
    data = parse_double_break(2)
    return sum(solve_for(line.split('\n')) for line in data)


def solve_for3(data):
    data = {k:[int(s) if s.isnumeric() else s for s in v.split(':')] for k,v in [line.split(' ') for line in data]}

    data['direction'] = [1 if d == 'CW' else -1 for d in data['direction']]

    print('\n', data)

    hand_ct = len(data['hands'])

    acc = 0

    # oh my god
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

    this_acc = 0
    for hand_index_a, hand_index_b in itertools.combinations(range(hand_ct), 2):
        temp_acc = 0

        seen = {}
        before_stop = True
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

        # print(f'{a_ticks}, {b_ticks} | {a_dir}, {b_dir} | {a_pos*hour_mult}, {b_pos*hour_mult} | {a_moves}, {b_moves}')
        print(f'{a_ticks}, {b_ticks} | {a_dir}, {b_dir} | {a_pos}, {b_pos} | {a_moves}, {b_moves}')

        second = 0
        seen[(a_pos, b_pos)] = 0
        while second < max_seconds:
            second += 1
            # print(f's{second}, a{a_pos}, b{b_pos}')

            a_start, b_start = a_pos, b_pos
            if second <= a_moves:
                a_pos += a_vel
                a_pos %= pair_mult
            if second <= b_moves:
                b_pos += b_vel
                b_pos %= pair_mult

            # collides_this_turn = collides(a_start*hour_mult, b_start*hour_mult, a_pos*hour_mult, b_pos*hour_mult, 12)
            collides_this_turn = collides(a_start, b_start, a_pos, b_pos, pair_mult)
            # print(a_pos, b_pos, collides_this_turn)
            if collides_this_turn:
                temp_acc += 1
            # print(a_pos*hour_mult, b_pos*hour_mult, collides(a_start, b_start, a_pos, b_pos, pair_mult))

            if second == min_seconds and min_seconds > 0:
                tick_until = 0
                seen = {}
                this_acc += temp_acc
                temp_acc = 0

            elif tick_until != 0:
                # print(second, tick_until)
                if second >= tick_until:
                    tick_until = 0
                    seen = {}
                    this_acc += temp_acc
                    print('limit reached; one hand stopped')
                    print('cleared seen and committed temp_acc which was', temp_acc)
                    print('now we should tick until another cycle')
                    temp_acc = 0

            elif (a_pos, b_pos) in seen:
                if second < min_seconds:
                    last_cycle = seen[(a_pos, b_pos)]
                    len_of_cycle = second - last_cycle
                    cycles_to_skip = (min_seconds - second - 1) // len_of_cycle
                    second_to_skip_to = second + len_of_cycle * cycles_to_skip

                    print('returned to start at second', second, 'meaning len of cycle is', len_of_cycle)
                    print('so we should skip', cycles_to_skip, 'cycles to end up at second', second_to_skip_to)
                    print('each cycle worth', temp_acc, 'so we count', temp_acc*cycles_to_skip, 'collisions')
                    print('now tick normally until cycle', min_seconds, '...')
                    tick_until = min_seconds
                    temp_acc *= cycles_to_skip + 1
                    print('temp_acc:', temp_acc)
                    second = second_to_skip_to

                else:
                    last_cycle = seen[(a_pos, b_pos)]
                    len_of_cycle = second - last_cycle
                    cycles_to_skip = (max_seconds - second) // len_of_cycle
                    second_to_skip_to = second + len_of_cycle * cycles_to_skip

                    print('found another cycle at', second, '; previous start was', last_cycle)
                    print('in that time we counted', temp_acc, 'collisions (should always be 1?)')
                    print('cycle length this time is', len_of_cycle)
                    print('we should skip', cycles_to_skip, 'cycles to end up at second', second_to_skip_to)
                    print('and then tick a few more times until we reach', max_seconds, 'seconds')
                    tick_until = max_seconds

                    temp_acc *= cycles_to_skip + 1
                    second = second_to_skip_to

            seen[(a_pos, b_pos)] = second

        print('hand pair', hand_index_a, hand_index_b, '=', temp_acc)
        this_acc += temp_acc
    print('finished all hand pairs')

    print('acc:', this_acc)
    # input()
    acc += this_acc

    print(acc)
    return acc

# 1128706431234 (len+char)...
# 1128186614160 not right either


def p3():
    data = parse_double_break(3)
    return sum(solve_for3(line.split('\n')) for line in data)


if __name__ == '__main__':
    setquest(13)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
