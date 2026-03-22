from ec import *


def p1():
    grid, inverse, unique = parse_grid(1)

    if verbose:
        print_2d('.', grid)

    pos = inverse['@'][0]
    tgt = inverse['#'][0]

    heading = 0
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    visited = {pos, }

    while True:
        next_pos = vadd(pos, dirs[heading])
        if next_pos not in visited:
            pos = next_pos
            if pos == tgt:
                return len(visited)
            visited.add(pos)
        heading = (heading + 1) % 4

        if verbose:
            print_2d(' ', {k: '+' for k in visited}, {pos: '@', tgt: '#'})
            print()


def p2():
    grid, inverse, unique = parse_grid(2)

    if verbose:
        print_2d('.', grid)

    pos = inverse['@'][0]
    tgt = inverse['#'][0]

    heading = 0
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    visited = {pos, tgt}

    def get_orth(p):
        return {vadd(x, p) for x in dirs}

    tgt_neighbors = get_orth(tgt)

    step = 0
    while True:
        next_pos = vadd(pos, dirs[heading])
        if next_pos not in visited:
            if not get_orth(next_pos) <= visited:
                pos = next_pos
                step += 1

            visited.add(next_pos)

            if tgt_neighbors <= visited:
                return step
        heading = (heading + 1) % 4

        if verbose:
            print_2d(' ', {k: '+' for k in visited}, {pos: '@', tgt: '#'})
            print()

# import time
def p3():
    grid, inverse, unique = parse_grid(3)

    if verbose:
        print_2d('.', grid)

    pos = inverse['@'][0]
    tgt = inverse['#']

    heading = 0
    dirs = [
        (0, -1), (0, -1), (0, -1),
        (1, 0), (1, 0), (1, 0),
        (0, 1), (0, 1), (0, 1),
        (-1, 0), (-1, 0), (-1, 0),
    ]

    visited = {pos, *tgt}

    def get_orth(p):
        return {vadd(x, p) for x in dirs}

    def try_flood_fill(start, bounds, limit=50):
        frontier = {start, }
        flood_visited = {start, }
        for i in range(limit):
            next_frontier = set()
            for pos in frontier:
                neighbors = get_orth(pos)
                for neighbor in neighbors:
                    if neighbor in flood_visited or neighbor in bounds:
                        continue
                    next_frontier.add(neighbor)
                    flood_visited.add(neighbor)
            if not next_frontier:
                return True, flood_visited
            else:
                frontier = next_frontier
        else:
            return False, flood_visited

    tgt_neighbors = set()
    for p in tgt:
        tgt_neighbors |= get_orth(p)

    if verbose:
        print('preprocessing...')
    for i, p in enumerate(tgt):
        if verbose:
            print(f'{i}/{len(tgt)}', end='   \r')
        to_check = [c for x in DIAGDIRS if (c := vadd(x, p)) not in visited]
        to_skip = set()
        for neighbor in to_check:
            if neighbor in to_skip:
                continue
            flood_result, flood_visited = try_flood_fill(neighbor, visited)
            if flood_result:
                visited |= flood_visited
            to_skip |= flood_visited
    if verbose:
        print('finished preprocessing.')

    step = 0
    while True:
        next_pos = vadd(pos, dirs[heading])
        heading = (heading + 1) % 12
        if next_pos in visited:
            continue

        pos = next_pos
        visited.add(pos)
        step += 1

        to_check = [c for x in DIAGDIRS if (c:=vadd(x, pos)) not in visited]
        to_skip = set()
        # print(to_check)

        for neighbor in to_check:
            if neighbor in to_skip:
                continue

            flood_result, flood_visited = try_flood_fill(neighbor, visited)
            # print(neighbor, flood_result, flood_visited)
            if flood_result:
                visited |= flood_visited

            to_skip |= flood_visited

        if verbose:
            print('\033c', end='', flush=False)
            print_2d(' ', {k: '+' for k in visited}, {k: '#' for k in tgt}, {pos: '@'})
            # input()
            # time.sleep(0.03)

        if tgt_neighbors <= visited:
            return step


setquest(2)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
