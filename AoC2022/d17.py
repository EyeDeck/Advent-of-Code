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


def next_dir(curr):
    r = data[curr]
    curr = (curr + 1) % len(data)
    return r, curr


def next_rock(lvl, curr):
    r = rocks[curr]
    curr = (curr + 1) % len(rocks)
    return {(x, y + lvl - 4): k for (x, y), k in r.items()}, curr


def move_rock(r, x_mod, y_mod):
    return {(x + x_mod, y + y_mod): k for (x, y), k in r.items()}


def can_move(r, board, x_mod, y_mod):
    for (x, y) in r:
        if (x + x_mod, y + y_mod) in board:
            return False
    return True


def p1():
    max_y = 0
    board = {(i, 0): '-' for i in range(-2, 5)}
    # board.update({(-3, i): '|' for i in range(-5, 0)})
    # board.update({(5, i): '|' for i in range(-5, 0)})
    # print_2d('.', board)
    # for rock_id in range(2022):
    data_index = 0
    rock_index = 0
    for rock_id in range(2022):
        for y in range(max_y - 6, max_y):
            board.update({(-3, y): '|', (5, y): '|'})

        rock, rock_index = next_rock(max_y, rock_index)
        # print('new rock:')
        # print_2d('.', board, rock)

        while True:
            next_jet, data_index = next_dir(data_index)
            # print(next_jet)

            next_jet = -1 if next_jet == '<' else 1
            if can_move(rock, board, next_jet, 0):
                rock = move_rock(rock, next_jet, 0)
                # print_2d('.', board, rock)

            if can_move(rock, board, 0, 1):
                rock = move_rock(rock, 0, 1)
                # print_2d('.', board, rock)
            else:
                break
        board.update(rock)
        max_y = min(max_y, min(i[1] for i in rock.keys()))
        # print(max_y)

        # input()

        # print(rock)

    # print_2d('.', board)

    return -max_y


def p2():
    magic = 1000000000000

    max_y = 0

    last_y = 0
    last_rock = 0

    last_y_diff = 0
    last_rock_diff = 0

    board = {(i, 0): '-' for i in range(-2, 5)}

    data_index = 0
    rock_index = 0
    cycle = len(data) * math.gcd(len(rocks), len(data))

    cycle_index = cycle

    stop_at = magic
    for rock_id in range(magic):
        stop_at -= 1
        if stop_at == 0:
            break

        for y in range(max_y - 6, max_y):
            board.update({(-3, y): '|', (5, y): '|'})

        rock, rock_index = next_rock(max_y, rock_index)

        while True:
            next_jet, data_index = next_dir(data_index)

            if cycle_index == 0:
                cycle_index = cycle
                rock_diff = rock_id - last_rock
                y_diff = max_y - last_y
                print(f'rock# {rock_id}, last {last_rock}, diff {rock_diff};  h {max_y}, last {last_y}, diff {y_diff}')
                # print('ct', rock_id, 'height', max_y, data_index, rock_index, 'diff', max_y - last_y)
                last_rock = rock_id
                last_y = max_y
                if rock_diff == last_rock_diff and y_diff == last_y_diff:
                    stop_at = (magic - rock_id) % rock_diff
                    print('cycle detected, doing another', stop_at, 'before calc')
                last_y_diff = y_diff
                last_rock_diff = rock_diff

            cycle_index -= 1

            next_jet = -1 if next_jet == '<' else 1
            if can_move(rock, board, next_jet, 0):
                rock = move_rock(rock, next_jet, 0)
                # print_2d('.', board, rock)

            if can_move(rock, board, 0, 1):
                rock = move_rock(rock, 0, 1)
                # print_2d('.', board, rock)
            else:
                break
        board.update(rock)
        max_y = min(max_y, min(i[1] for i in rock.keys()))

    # print_2d('.', board)
    return -max_y + -(((magic - last_rock) // last_rock_diff) * last_y_diff)


day = 17
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [c for c in file.read().strip()]

print('part1:', p1())
print('part2:', p2())
