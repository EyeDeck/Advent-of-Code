from ec import *


def test_cell(Xv, Yv, Xc, Yc, R):
    return (Xv - Xc) * (Xv - Xc) + (Yv - Yc) * (Yv - Yc) <= R * R


def get_cells(center, r):
    vX, vY = center
    cells = set()
    for x in range(vX - r, vX + r + 1):
        for y in range(vY - r, vY + r + 1):
            if test_cell(*center, x, y, r):
                cells.add((x, y))
    return cells


def p1():
    grid, inverse, unique = parse_grid(1)
    volcano = unique['@']
    eruption_mask = get_cells(volcano, 10)
    print_2d('.', {k: grid[k] for k in eruption_mask})
    return sum(int(grid[c]) for c in eruption_mask - {volcano, })


def p2():
    grid, inverse, unique = parse_grid(2)
    volcano = unique['@']
    cur_set = set()
    max_destruction = 0
    max_index = 0
    for i in range(100):
        eruption_mask = get_cells(volcano, i)
        unique_mask = eruption_mask - cur_set
        cur_set = eruption_mask
        destruction = sum((int(grid[c]) if c in grid else 0) for c in unique_mask - {volcano, })
        if destruction > max_destruction:
            max_destruction = destruction
            max_index = i
    return max_destruction * max_index


dirs = {
    'R': (1, 0),
    'U': (0, -1),
    'L': (-1, 0),
    'D': (0, 1),
}


def get_quadrant_dirs(center, pos):
    cX, cY = center
    pX, pY = pos
    if pX < cX:
        if pY < cY:  # top left
            return [dirs['L'], dirs['D']]
        else:  # top right
            return [dirs['L'], dirs['U']]
    else:
        if pY < cY:  # bottom left
            return [dirs['D'], dirs['R']]
        else:  # bottom right
            return [dirs['U'], dirs['R']]


def wbfs(src, tgt, edges, nodes, blocked_nodes):
    """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
    a list of `(node, cost)` pairs."""
    q = [(0, src, None)]

    cost = 0
    parent = {}

    while q:
        cost, cur, prev = heapq.heappop(q)
        if cur in parent:
            continue
        parent[cur] = prev
        if cur == tgt:
            break

        for (n, ncost) in edges(cur, nodes, blocked_nodes):
            if n in parent:
                continue
            heapq.heappush(q, (cost + ncost, n, cur))

    if tgt not in parent:
        return None

    pos = tgt
    path = []
    while pos != src:
        path.append(pos)
        pos = parent[pos]
    path.append(src)
    path.reverse()
    return cost, path


def get_neighbors(pos, nodes, blocked_nodes):
    n = []
    for d in DIRS:
        c = vadd(d, pos)
        if c in nodes and c not in blocked_nodes:
            n.append((c, nodes[c]))
    return n


# def p3():
#     grid, inverse, unique = parse_grid(3)
#
#     volcano = unique['@']
#     start = unique['S']
#     bounds = grid_bounds(grid)
#
#     volcano_cost = {k:int(v) for k,v in grid.items() if v.isnumeric()}
#     volcano_cost[start] = 0
#     left_slice = {(x,volcano[1]):0 for x in range(volcano[0]-1, -1, -1)}
#     down_slice = {(volcano[0],y):0 for y in range(volcano[1]+1, bounds[3]+1)}
#     right_slice = {(x,volcano[1]):0 for x in range(volcano[0]+1, bounds[2]+1)}
#
#     a_list = bresenham(volcano[0]-1, volcano[1], 0, bounds[3])
#     b_list = bresenham(volcano[0]+1, volcano[1], bounds[2], bounds[3])
#
#     print((0, bounds[3]), (volcano[0]-1, volcano[1]), a_list)
#     print((volcano[0]+1, volcano[1]), (bounds[2], bounds[3]), b_list)
#
#     print_2d('.', grid, {k:'A' for k in a_list}, {k:'B' for k in b_list}) # , {k:'C' for k in c_list})
#
#     print(volcano, a_list)
#     print(bounds)
#
#
#
#     print(wbfs(start, vadd(volcano,(-1,-1)), get_neighbors, INF))
#
#     # print(
#     #     wbfs(start, (7, 3), get_neighbors, INF),
#     #     wbfs((7,3), vadd(volcano,(-1,-1)), get_neighbors, INF)
#     # )
#
#     for radius in range(5, vdistm(volcano, start)):
#         impassable = get_cells(volcano, radius)
#         for c in impassable:
#             volcano_cost.pop(c, None)
#         print(f'checking radius {radius}, remaining volcano cells {len(volcano_cost)}')
#         for a in a_list:
#             if a in impassable:
#                 continue
#             result = wbfs(start, a, get_neighbors, radius*30)
#             if result is None:
#                 # print(f'no path from {start} to {a} at radius {radius}')
#                 continue
#             cost_to_a, path_to_a = result
#
#             print(f'{start} to {a} at radius {radius} = {cost_to_a}')
#
#             for b in b_list:
#                 if b in impassable:
#                     continue
#                 result = wbfs(a, b, get_neighbors, (radius * 30) - cost_to_a)
#                 if result is None:
#                     # print(f'no path from {start} to {a} at radius {radius}')
#                     continue
#                 cost_to_b, path_to_b = result
#
#                 result = wbfs(b, start, get_neighbors, (radius * 30) - (cost_to_a + cost_to_b))
#                 if result is None:
#                     continue
#                 print('found path!!')
#                 cost_to_start, path_to_start = result
#
#                 print_2d('.',
#                          volcano_cost,
#                          {k: 'A' for k in path_to_a},
#                          {k: 'B' for k in path_to_b},
#                          {k: 'C' for k in path_to_start}
#                          )
#
#                 return cost_to_a, cost_to_b, cost_to_start, (cost_to_a + cost_to_b + cost_to_start), radius, (cost_to_a + cost_to_b + cost_to_start) * radius
#
#
#     return


def p3():
    grid, inverse, unique = parse_grid(3)

    volcano = unique['@']
    start = unique['S']
    bounds = grid_bounds(grid)

    volcano_cost = {k: int(v) for k, v in grid.items() if v.isnumeric()}
    volcano_cost[start] = 0
    left_slice = {(x, volcano[1]): 0 for x in range(volcano[0] - 1, -1, -1)}
    down_slice = {(volcano[0], y): 0 for y in range(volcano[1] + 1, bounds[3] + 1)}
    right_slice = {(x, volcano[1]): 0 for x in range(volcano[0] + 1, bounds[2] + 1)}

    a_list = bresenham(volcano[0] - 1, volcano[1], 0, bounds[3])
    b_list = bresenham(volcano[0] + 1, volcano[1], bounds[2], bounds[3])

    print((0, bounds[3]), (volcano[0] - 1, volcano[1]), a_list)
    print((volcano[0] + 1, volcano[1]), (bounds[2], bounds[3]), b_list)

    # print_2d('.', grid, {k: 'A' for k in a_list}, {k: 'B' for k in b_list})  # , {k:'C' for k in c_list})

    print(volcano, a_list)
    print(bounds)

    # print(wbfs(start, vadd(volcano, (-1, -1)), get_neighbors, INF))

    # print(
    #     wbfs(start, (7, 3), get_neighbors, INF),
    #     wbfs((7,3), vadd(volcano,(-1,-1)), get_neighbors, INF)
    # )

    print_2d(' ', {k:'.' for k in get_cells(volcano, 1)})

    for radius in range(1, vdistm(volcano, start)):
        impassable = get_cells(volcano, radius)
        for c in impassable:
            volcano_cost.pop(c, None)
        print(f'checking radius {radius}, remaining volcano cells {len(volcano_cost)}')
        for a in down_slice:
            if a in impassable:
                continue
            result = wbfs(start, a, get_neighbors, volcano_cost, right_slice, radius * 30)
            if result is None:
                # print(f'no path from {start} to {a} at radius {radius}')
                continue
            cost_to_a, path_to_a = result

            print(f'{start} to {a} at radius {radius} = {cost_to_a}')
            print_2d(' ', {k:'.' for k in impassable}, {k:volcano_cost[k] for k in path_to_a})

            result = wbfs(a, start, get_neighbors, volcano_cost, left_slice, radius * 30 - cost_to_a)
            print(f'remaining cost: {radius * 30 - cost_to_a}')

            if result is None:
                print(f'no path from {start} to {a} at radius {radius}')
                continue
            cost_to_start, path_to_start = result

            print('found path!!')

            print_2d('.',
                     volcano_cost,
                     {k: 'A' for k in path_to_a},
                     # {k: 'B' for k in path_to_b},
                     {k: 'C' for k in path_to_start}
                     )

            return cost_to_a, cost_to_start, (cost_to_a + cost_to_start), radius, (cost_to_a + cost_to_start) * (radius)

    return



def p3():
    grid, inverse, unique = parse_grid(3)

    volcano = unique['@']
    start = unique['S']
    bounds = grid_bounds(grid)

    volcano_cost = {k: int(v) for k, v in grid.items() if v.isnumeric()}
    volcano_cost[start] = 0
    left_slice = {(x, volcano[1]): 0 for x in range(volcano[0] - 1, -1, -1)}
    down_slice = {(volcano[0], y): 0 for y in range(volcano[1] + 1, bounds[3] + 1)}
    right_slice = {(x, volcano[1]): 0 for x in range(volcano[0] + 1, bounds[2] + 1)}

    a_list = bresenham(volcano[0] - 1, volcano[1], 0, bounds[3])
    b_list = bresenham(volcano[0] + 1, volcano[1], bounds[2], bounds[3])

    print((0, bounds[3]), (volcano[0] - 1, volcano[1]), a_list)
    print((volcano[0] + 1, volcano[1]), (bounds[2], bounds[3]), b_list)

    # print_2d('.', grid, {k: 'A' for k in a_list}, {k: 'B' for k in b_list})  # , {k:'C' for k in c_list})

    print(volcano, a_list)
    print(bounds)

    # print(wbfs(start, vadd(volcano, (-1, -1)), get_neighbors, INF))

    # print(
    #     wbfs(start, (7, 3), get_neighbors, INF),
    #     wbfs((7,3), vadd(volcano,(-1,-1)), get_neighbors, INF)
    # )

    print_2d(' ', {k:'.' for k in get_cells(volcano, 1)})

    radius = 0
    last_cost = -1
    impassable = {}

    while True:
        print('working on radius {radius}')
        lowest_cost = INF
        shortest_path = None

        for a in down_slice:
            if a in impassable:
                continue

            result = wbfs(start, a, get_neighbors, volcano_cost, right_slice)
            if result is None:
                # print(f'no path from {start} to {a} at radius {radius}')
                continue
            cost_to_a, path_to_a = result

            # print(f'{start} to {a} at radius {radius} = {cost_to_a}')
            # print_2d(' ', {k:'.' for k in impassable}, {k:volcano_cost[k] for k in path_to_a})

            result = wbfs(a, start, get_neighbors, volcano_cost, left_slice)
            if result is None:
                # print(f'no path from {start} to {a} at radius {radius}')
                continue
            cost_to_start, path_to_start = result
            total_cost = cost_to_a + cost_to_start
            whole_path = path_to_a + path_to_start
            # print(f'minimum loop cost: {total_cost}')

            # print(lowest_cost)
            if total_cost < lowest_cost:
                lowest_cost = total_cost
                shortest_path = whole_path

        if lowest_cost != INF:
            print_2d('.',volcano_cost, {k: '-' for k in whole_path} )

            radius = (lowest_cost) // 30

            impassable = get_cells(volcano, radius)
            for c in impassable:
                volcano_cost.pop(c, None)

            if shortest_path:
                for c in shortest_path:
                    if c in impassable:
                        break
                else:
                    return radius, lowest_cost, radius * lowest_cost
        else:
            radius += 1
        # print(f'checking radius {radius}, remaining volcano cells {len(volcano_cost)}')


    return


setquest(17)

# print('part1:', p1())
# print('part2:', p2())
print('part3:', p3())
