import sys


def run_n_times(data, ct, start_append, neighbor_func):
    running = set()
    for x, line in enumerate(data):
        for y, tile in enumerate(line):
            if tile:
                running.add((x, y) + start_append)
    for i in range(0, ct):
        running = step(running, neighbor_func)
    return len(running)


def get_neighbors_3d(x, y, z, bd, get_all=False):
    neighbors = set()
    for x2 in range(x - 1, x + 2):
        for y2 in range(y - 1, y + 2):
            for z2 in range(z - 1, z + 2):
                if (get_all or ((x2, y2, z2) in bd)) and (x, y, z) != (x2, y2, z2):
                    neighbors.add((x2, y2, z2))
    return neighbors


def get_neighbors_4d(x, y, z, w, bd, get_all=False):
    neighbors = set()
    for x2 in range(x - 1, x + 2):
        for y2 in range(y - 1, y + 2):
            for z2 in range(z - 1, z + 2):
                for w2 in range(w - 1, w + 2):
                    if (get_all or ((x2, y2, z2, w2) in bd)) and (x, y, z, w) != (x2, y2, z2, w2):
                        neighbors.add((x2, y2, z2, w2))
    return neighbors


def step(bd, neighbor_func):
    new_board = set()
    to_tick = set()
    for cell in bd:
        to_tick.update(neighbor_func(*cell, bd, True))
    print('cells to tick', len(to_tick))
    for cell in to_tick:
        n_ct = len(neighbor_func(*cell, bd))
        if cell in bd:
            if n_ct == 2 or n_ct == 3:
                new_board.add(cell)
        else:
            if n_ct == 3:
                new_board.add(cell)
    return new_board


f = 'd17.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[True if x == '#' else False for x in line.strip()] for line in file]

print(f'part1: {run_n_times(data, 6, (0,), get_neighbors_3d):}')
print(f'part2: {run_n_times(data, 6, (0, 0), get_neighbors_4d):}')
