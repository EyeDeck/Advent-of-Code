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
# for rock in rocks.values():
#     # print(rock)
#     print_2d('.', rock)
#     print()


CURR_DIR = 0
CURR_ROCK = 0


def next_dir():
    global CURR_DIR
    r = data[CURR_DIR]
    CURR_DIR += 1
    if CURR_DIR >= len(data):
        CURR_DIR = 0
    # print('!', data[CURR_DIR], CURR_DIR)
    return r


def next_rock(lvl):
    global CURR_ROCK
    r = rocks[CURR_ROCK]
    CURR_ROCK += 1
    if CURR_ROCK >= len(rocks):
        CURR_ROCK = 0
    # print(rocks[CURR_ROCK])
    return {(x, y + lvl - 4): k for (x, y), k in r.items()}


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
    for rock_id in range(len(data) * 3):
        for y in range(max_y - 6, max_y):
            board.update({(-3, y): '|', (5, y): '|'})

        rock = next_rock(max_y)
        # print('new rock:')
        # print_2d('.', board, rock)

        while True:
            next_jet = next_dir()
            # print(next_jet)

            if CURR_DIR == 0:
                board[8, max_y] = '<'

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
    max_y = 0

    last_y = 0
    last_rock = 0

    last_y_diff = 0
    last_rock_diff = 0

    board = {(i, 0): '-' for i in range(-2, 5)}
    # board.update({(-3, i): '|' for i in range(-5, 0)})
    # board.update({(5, i): '|' for i in range(-5, 0)})
    # print_2d('.', board)
    # for rock_id in range(2022):
    stop_at = 100000000000
    for rock_id in range(100000000):
        stop_at -= 1
        if stop_at == 0:
            break
        # if rock_id == stop_at:
        #     break

        for y in range(max_y - 6, max_y):
            board.update({(-3, y): '|', (5, y): '|'})

        rock = next_rock(max_y)
        # print('new rock:')
        # print_2d('.', board, rock)

        while True:
            next_jet = next_dir()
            # print(next_jet)

            if CURR_DIR == 0:  # and CURR_ROCK == 0:
                # board[8, max_y] = '<'
                rock_diff = rock_id - last_rock
                y_diff = max_y - last_y
                print(f'rock# {rock_id}, last {last_rock}, diff {rock_diff};  h {max_y}, last {last_y}, diff {y_diff}')
                # print('ct', rock_id, 'height', max_y, CURR_DIR, CURR_ROCK, 'diff', max_y - last_y)
                last_rock = rock_id
                last_y = max_y
                # print(rock_diff, last_rock_diff, y_diff, last_y_diff)
                if rock_diff == last_rock_diff and y_diff == last_y_diff:
                    stop_at = (1000000000000 - rock_id) % rock_diff
                    print('cycle detected', stop_at)
                last_y_diff = y_diff
                last_rock_diff = rock_diff

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

    return -max_y + -(((1000000000000 - last_rock) // last_rock_diff) * last_y_diff)
# 1514285714288
# 1589142865526 too high
# 1589142857183
# 529411774004


day = 17
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [c for c in file.read().strip()]
    # print(data)

print('part1:', p1())
print('part2:', p2())
