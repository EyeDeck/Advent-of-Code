from aoc import *

def get_tile(x, y, inp):
    return int.bit_count((x * x + 3 * x + 2 * x * y + y + y * y) + inp) & 1

def get_neighbors(c):
    neighbors = [vadd(c, dir) for dir in DIRS]
    neighbors = [(n, 1) for n in neighbors if not get_tile(*n, data) and n[0] >= 0 and n[1] >= 0]
    return neighbors

def p1():
    target = (31,39)
    # target = (7,4)
    r = wbfs((1,1), target, get_neighbors)

    print_2d(' ', {(x, y): '#' if get_tile(x, y, data) else '.' for x in range(target[0]+3) for y in range(target[1]+3)}, {k:'O' for k in r})
    return len(r)-1


def p2():
    frontier = [(1,1)]
    seen = set()
    for step in range(50):
        new_frontier = []
        for node in frontier:
            neighbors = get_neighbors(node)
            for neighbor in neighbors:
                neighbor = neighbor[0]
                if neighbor in seen:
                    continue
                new_frontier.append(neighbor)
                seen.add(neighbor)
        frontier = new_frontier

    print_2d(' ', {(x, y): '#' if get_tile(x, y, data) else '.' for x in range(max(seen, key=itemgetter(0))[0]+1) for y in range(max(seen, key=itemgetter(1))[1]+1)}, {k: 'O' for k in seen})
    return len(seen)


setday(13)

data = int(parselines()[0])
# data = 10

print('part1:', p1() )
print('part2:', p2() )
