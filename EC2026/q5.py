from ec import *


def p1():
    grid, inverse, unique = parse_grid(1)

    center = tuple(n//2 for n in max(grid))
    print_2d(' ', grid, {center:'#'})
    print(center)
    land = {center,}
    frontier = {center,}
    while frontier:
        new_land = set()
        new_frontier = set()
        for pos in frontier:
            neighbors = [vadd(pos, d) for d in DIAGDIRS]
            neighbors = [c for c in neighbors if c not in land]
            # print(neighbors)
            ct = 0
            for n in neighbors:
                nn = [vadd(n, d) for d in DIAGDIRS]
                nn = [1 if (c in land or (c in grid and grid[c]=='1')) else 0 for c in nn]
                # print(n, nn, sum(nn))
                if sum(nn) >= 5:
                    new_frontier.add(n)
                    new_land.add(n)
        land |= new_land
        frontier = new_frontier

        # print(land, frontier)

        disp = {k:'~' for k in land}
        if frontier:
            disp |= {k: '#' for k in frontier}
        print_2d(' ', disp)
        # input()

    return len(land)


def p2():
    grid, inverse, unique = parse_grid(2)

    center = tuple(n//2 for n in max(grid))
    print_2d(' ', grid, {center:'#'})
    print(center)
    land = {center,}
    frontier = {center,}
    while frontier:
        new_land = set()
        new_frontier = set()
        for pos in frontier:
            neighbors = [vadd(pos, d) for d in DIAGDIRS]
            neighbors = [c for c in neighbors if c not in land]
            # print(neighbors)
            ct = 0
            for n in neighbors:
                nn = [vadd(n, d) for d in DIAGDIRS]
                nn = [1 if (c in land or (c in grid and grid[c]=='1')) else 0 for c in nn]
                # print(n, nn, sum(nn))
                if sum(nn) >= 5:
                    new_frontier.add(n)
                    new_land.add(n)
        land |= new_land
        frontier = new_frontier

        # print(land, frontier)

        disp = {k:'~' for k in land}
        if frontier:
            disp |= {k: '#' for k in frontier}
        print_2d(' ', disp)

    sand = set()
    for pos in land:
        neighbors = [vadd(pos, d) for d in DIAGDIRS]
        neighbors = [c for c in neighbors if c not in land]
        if len(neighbors) > 0:
            sand.add(pos)

    print_2d(' ', {k: '#' for k in land}, {k: '=' for k in sand})

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
            break

    return len(sand)


def p3():
    grid, inverse, unique = parse_grid(3)

    center = tuple(n//2 for n in max(grid))
    print_2d(' ', grid, {center:'#'})
    print(center)
    land = {center,}
    frontier = {center,}
    while frontier:
        new_land = set()
        new_frontier = set()
        for pos in frontier:
            neighbors = [vadd(pos, d) for d in DIAGDIRS]
            neighbors = [c for c in neighbors if c not in land]
            # print(neighbors)
            ct = 0
            for n in neighbors:
                nn = [vadd(n, d) for d in DIAGDIRS]
                nn = [1 if (c in land or (c in grid and grid[c]=='1')) else 0 for c in nn]
                # print(n, nn, sum(nn))
                if sum(nn) >= 5:
                    new_frontier.add(n)
                    new_land.add(n)
        land |= new_land
        frontier = new_frontier

        # print(land, frontier)

        # disp = {k:'~' for k in land}
        # if frontier:
        #     disp |= {k: '#' for k in frontier}
        # print_2d(' ', disp)

    sand = set()
    for pos in land:
        neighbors = [vadd(pos, d) for d in DIAGDIRS]
        neighbors = [c for c in neighbors if c not in land]
        if len(neighbors) > 0:
            sand.add(pos)

    # print_2d(' ', {k: '#' for k in land}, {k: '=' for k in sand})

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
            break

    land -= sand
    print_2d(' ', {k: '#' for k in land}, {k: '=' for k in sand})

    trees = set()
    for pos in land:
        neighbors = []
        for x in range(-2,3):
            for y in range(-2,3):
                if abs(x) + abs(y) == 4:
                    continue
                neighbors.append(vadd((x,y), pos))
        if all(c in land for c in neighbors):
            trees.add(pos)

    land -= trees

    print_2d(' ', {k: '#' for k in land}, {k: '=' for k in sand}, {k: '@' for k in trees})

    for _ in range(2):
        new_trees = set()
        for pos in land:
            neighbors = [vadd(pos, d) for d in DIAGDIRS]
            if any(c in sand for c in neighbors):
                continue
            if sum(1 for c in neighbors if c in trees) >= 4:
                new_trees.add(pos)
        trees |= new_trees
        land -= trees
        print_2d(' ', {k: '#' for k in land}, {k: '=' for k in sand}, {k: '@' for k in trees})

    return len(trees)


if __name__ == '__main__':
    setquest(5)

    # print('part1:', p1())
    # print('part2:', p2())
    print('part3:', p3())
