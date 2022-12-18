import math
import sys
from aoc import print_2d

rocks_raw = '''####

.#.
###
.#.

###
..#
..#

#
#
#
#

##
##'''
rocks = {}
for id, rock in enumerate(rocks_raw.split('\n\n')):
    rocks[id] = {}
    for y, line in enumerate(rock.split('\n')):
        for x, c in enumerate(line):
            if c == '#':
                rocks[id][x, -y] = '#'


def solve(magic):
    def next_dir():
        nonlocal data_index
        r = data[data_index]
        data_index = (data_index + 1) % len(data)
        return r

    def next_rock(lvl):
        nonlocal rock_index
        r = rocks[rock_index]
        rock_index = (rock_index + 1) % len(rocks)
        return {(x, y + lvl - 4): k for (x, y), k in r.items()}

    def move_rock(r, x_mod, y_mod):
        return {(x + x_mod, y + y_mod): k for (x, y), k in r.items()}

    def can_move(r, x_mod, y_mod):
        for (x, y) in r:
            if (x + x_mod, y + y_mod) in board:
                return False
        return True

    max_y = 0

    last_y = 0
    last_rock = 0

    last_y_diff = 0
    last_rock_diff = 0

    board = {(i, 0): '-' for i in range(-2, 5)}

    data_index = 0
    rock_index = 0
    cycle = len(data) * math.gcd(len(rocks), len(data))
    found_cycle = False

    cycle_index = cycle

    stop_after = magic
    for rock_id in range(magic):
        if stop_after == 0:
            break

        for y in range(max_y - 6, max_y):
            board.update({(-3, y): '|', (5, y): '|'})

        rock = next_rock(max_y)

        while True:
            next_jet = next_dir()

            if cycle_index == 0:
                cycle_index = cycle
                rock_diff = rock_id - last_rock
                y_diff = max_y - last_y
                print(f'rock# {rock_id}, last {last_rock}, diff {rock_diff};  h {max_y}, last {last_y}, diff {y_diff}')
                last_rock = rock_id
                last_y = max_y
                if rock_diff == last_rock_diff and y_diff == last_y_diff:
                    stop_after = (magic - rock_id) % rock_diff
                    found_cycle = True
                    print('cycle detected, doing another', stop_after, 'before calc')
                last_y_diff = y_diff
                last_rock_diff = rock_diff

            cycle_index -= 1

            next_jet = -1 if next_jet == '<' else 1
            if can_move(rock, next_jet, 0):
                rock = move_rock(rock, next_jet, 0)
                # print_2d('.', board, rock)

            if can_move(rock, 0, 1):
                rock = move_rock(rock, 0, 1)
                # print_2d('.', board, rock)
            else:
                break
        board.update(rock)
        max_y = min(max_y, min(i[1] for i in rock.keys()))
        
        stop_after -= 1

    # print_2d('.', board, constrain=(-4000, -4000, 4000, 4000))
    return -max_y + (-(((magic - last_rock) // last_rock_diff) * last_y_diff) if found_cycle else 0)


day = 17
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [c for c in file.read().strip()]

print('part1:', solve(2022))
print('part2:', solve(1000000000000))
