import sys


def find_loop(key, subj, mod):
    v = 1
    for i in range(1, mod):
        v = v * subj % mod
        if v == key:
            return i


def run_loop(subj, loops, mod):
    v = 1
    for i in range(loops):
        v = v * subj % mod
    return v


def p1():
    mod = 20201227
    card_public, door_public = data

    card_loop = find_loop(card_public, 7, mod)
    door_loop = find_loop(door_public, 7, mod)

    card_key = run_loop(door_public, card_loop, mod)
    door_key = run_loop(card_public, door_loop, mod)

    assert card_key == door_key
    return card_key


f = 'd25.txt'
assert len(sys.argv) <= 3
if len(sys.argv) == 2:
    f = sys.argv[1]
elif len(sys.argv) == 3:
    data = [int(i) for i in sys.argv[1:]]
if len(sys.argv) <= 2:
    with open(f) as file:
        data = [int(line.strip()) for line in file]


print(f'part1: {p1()}')
