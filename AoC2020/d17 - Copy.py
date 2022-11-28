import sys


def p1(bd):
    running = bd
    for i in range(0,6):
        running = step(running)
    print('end', running)
    return len(running)


def p2():
    return None


def get_neighbors(x, y, z, bd, get_all=False):
    neighbors = set()
    # print('GIVEN', x,y,z)
    for x2 in range(x-1, x+2):
        for y2 in range(y-1, y+2):
            for z2 in range(z-1, z+2):
                # print(board, 'checking', (x,y,z), ((x,y,z) in board))
                if (get_all or ((x2,y2,z2) in bd)) and (x,y,z) != (x2,y2,z2):
                    neighbors.add((x2,y2,z2))
    return neighbors


def step(bd):
    new_board = set()
    to_tick = set()
    for cell in bd:
        to_tick.update(get_neighbors(*cell, bd, True))
        # print('aaaaa', get_neighbors(*cell, True))
    print('cells to tick', len(to_tick))
    for cell in to_tick:
        # print('ticking', cell)
        n_ct = len(get_neighbors(*cell, bd))
        # print('ng', n_ct)
        if cell in bd:
            if n_ct == 2 or n_ct == 3:
                new_board.add(cell)
        else:
            if n_ct == 3:
                new_board.add(cell)
    return new_board

# 0 1 0 0
# 0 0 0 2
# 0 0 2 0
# 0 0 0 0

# {(1, 0, 1), (2, 2, 1), (3, 1, 1)
# (1, 2, 0), (2, 1, 0), (3, 1, 0), (1, 0, 0), (2, 2, 0),
# (1, 0, -1), (2, 2, -1), , (3, 1, -1)}

f = 'd17.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[True if x == '#' else False for x in line.strip()] for line in file]

# board = defaultdict(bool)
board = set()
for x_, line in enumerate(data):
    for y_, tile in enumerate(line):
        if tile:
            board.add((x_,y_,0))

print(board)
# board = np.zeros((21,21,21), dtype=bool)
# print(board)


print(f'part1: {p1(board)}')
print(f'part2: {p2()}')
