from collections import *
from aoc import *

# somehow I ended up needing all of these
DIRS = [
    (1, 0),  # r
    (0, 1),  # d
    (-1, 0),  # l
    (0, -1),  # u
]
DIRS_C = ['>', 'v', '<', '^']
DIRS_C_R = ['<', '^', '>', 'v']
DIRS_R = {'>': 0, 'v': 1, '<': 2, '^': 3}

reset_pos = {
    '>': lambda x, y: (bounds[0] + 1, y),
    'v': lambda x, y: (x, bounds[1] + 1),
    '<': lambda x, y: (bounds[2] - 1, y),
    '^': lambda x, y: (x, bounds[3] - 1),
}


def tick(blizzards):
    new_blizzards = defaultdict(list)
    for tile, b in blizzards.items():
        for blizzard in b:
            # print(tile, blizzard)

            next_pos = vadd(tile, DIRS[DIRS_R[blizzard]])
            # print(next_pos)
            if next_pos in walls:
                next_pos = reset_pos[blizzard](*tile)

            new_blizzards[next_pos].append(blizzard)
    return new_blizzards


def get_neighbors(c, b, walls):
    neighbors = [c]
    for i, dir in enumerate(DIRS):
        n = vadd(dir, c)
        if n in b:
            continue
        if n in walls:
            continue
        neighbors.append(n)
    return neighbors


def traverse_maze(blizz, start, end):
    positions = {start}

    # print('Initial state:')
    # print_2d(
    #     '. ', {(x, y): (b[0] if len(b) == 1 else len(b)) for (x, y), b in blizz.items()},
    #     {(x, y): '#' for x, y in walls}
    # )

    minute = 0
    while True:
        minute += 1

        next_blizz = tick(blizz)
        next_positions = set()

        positions = {p for p in positions if p not in blizz}

        # print(f'Minute {minute}')
        # print_2d(
        #     '. ', {(x, y): (b[0] if len(b) == 1 else len(b)) for (x, y), b in blizz.items()},
        #     {(x, y): '#' for x, y in walls},
        #     {c: '@' for c in positions}
        # )

        while positions:
            cur = positions.pop()

            if cur == end:
                return minute, blizz

            for n in get_neighbors(cur, next_blizz, walls):
                next_positions.add(n)

        positions = next_positions
        blizz = next_blizz

        if not positions:
            return None


def p1():
    m, _ = traverse_maze(tick(blizzards), start, end)
    return m


def p2():
    tgts = [[start, end], [end, start], [start, end]]
    b = blizzards
    minutes = 0
    for s, e in tgts:
        m, b = traverse_maze(tick(b), s, e)
        minutes += m
    return minutes


day = 24
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

blizzards = defaultdict(list)
empty = set()
walls = set()
with open(f) as file:
    for y, line in enumerate(file.readlines()):
        for x, c in enumerate(line.strip()):
            if c == '#':
                walls.add((x, y))
            elif c in '<>^v':
                blizzards[x, y].append(c)
            elif c == '.':
                empty.add((x, y))

start, end = min(empty, key=itemgetter(1)), max(empty, key=itemgetter(1))

bounds = min(walls, key=itemgetter(0))[0], min(walls, key=itemgetter(1))[1], \
         max(walls, key=itemgetter(0))[0], max(walls, key=itemgetter(1))[1]

walls.add((start[0], start[1] - 1))
walls.add((end[0], end[1] + 1))

print('part1:', p1())
print('part2:', p2())
