from ec import *


def find_land(grid):
    center = tuple(n // 2 for n in max(grid))
    land = {center, }
    frontier = {center, }
    while frontier:
        new_land = set()
        new_frontier = set()
        for pos in frontier:
            neighbors = [vadd(pos, d) for d in DIAGDIRS]
            neighbors = [c for c in neighbors if c not in land]
            for n in neighbors:
                nn = [vadd(n, d) for d in DIAGDIRS]
                nn = [1 if (c in land or (c in grid and grid[c] == '1')) else 0 for c in nn]
                if sum(nn) >= 5:
                    new_frontier.add(n)
                    new_land.add(n)
        land |= new_land
        frontier = new_frontier

    return land


def find_sand(land):
    sand = set()
    for pos in land:
        neighbors = [vadd(pos, d) for d in DIAGDIRS]
        neighbors = [c for c in neighbors if c not in land]
        if len(neighbors) > 0:
            sand.add(pos)

    while True:
        new_sand = set()
        for pos in sand:
            neighbors = [vadd(pos, d) for d in DIAGDIRS]
            for n in neighbors:
                if n not in land or n in sand:
                    continue
                nn = [vadd(n, d) for d in DIAGDIRS]
                nn = [1 if c in sand else 0 for c in nn]
                if sum(nn) >= 5:
                    new_sand.add(n)
        if new_sand:
            sand |= new_sand
        else:
            return sand


def plant_trees(land):
    trees = set()
    for pos in land:
        stamp = {vadd(pos, (x,y)) for x in range(-2,3) for y in range(-2,3) if abs(x) + abs(y) != 4}
        if stamp.issubset(land):
            trees.add(pos)
    return trees


def tick_trees(land, sand, trees):
    new_trees = set()
    for pos in land:
        neighbors = [vadd(pos, d) for d in DIAGDIRS]
        if any(c in sand for c in neighbors):
            continue
        if sum(1 for c in neighbors if c in trees) >= 4:
            new_trees.add(pos)
    trees |= new_trees
    land -= trees


def p1():
    grid, inverse, unique = parse_grid(1)

    land = find_land(grid)

    if verbose:
        print_2d('.', grid, {k: '#' for k in land})

    return len(land)


def p2():
    grid, inverse, unique = parse_grid(2)

    land = find_land(grid)
    sand = find_sand(land)
    land -= sand

    if verbose:
        print_2d(' ', grid, {k: '#' for k in land}, {k: '=' for k in sand})

    return len(sand)


def p3():
    grid, inverse, unique = parse_grid(3)

    land = find_land(grid)
    sand = find_sand(land)
    land -= sand

    trees = plant_trees(land)
    land -= trees

    for _ in range(2):
        tick_trees(land, sand, trees)

    if verbose:
        print_2d(' ', {k: '#' for k in land}, {k: '=' for k in sand}, {k: '@' for k in trees})

    return len(trees)


if __name__ == '__main__':
    setquest(5)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
