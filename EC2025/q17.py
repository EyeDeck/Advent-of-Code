import math

from ec import *


def test_cell(Xv, Yv, Xc, Yc, R):
    # using the function from the puzzle description verbatim
    return (Xv - Xc) * (Xv - Xc) + (Yv - Yc) * (Yv - Yc) <= R * R


def get_cells(center, r):
    v_x, v_y = center
    cells = set()
    for x in range(v_x - r, v_x + r + 1):
        for y in range(v_y - r, v_y + r + 1):
            if test_cell(*center, x, y, r):
                cells.add((x, y))
    return cells


def p1():
    grid, inverse, unique = parse_grid(1)
    volcano = unique['@']
    eruption_mask = get_cells(volcano, 10)
    if verbose:
        print(f'part 1 circle:')
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


def wbfs(src, tgt, edges, nodes, blocked_nodes):
    # modified from library version to return cost, so I don't have to recalc it
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


def p3():
    grid, inverse, unique = parse_grid(3)

    volcano = unique['@']
    start = unique['S']
    bounds = grid_bounds(grid)

    vector = vsub(start, volcano)
    length = math.hypot(*vector)
    unit = vdiv(vector, (length)*2)
    max_side_len = max(bounds[1:])
    seg_len = max_side_len * math.sqrt(2)

    offset = tuple(round(f) for f in vmul(unit, (seg_len,)*2))
    opposite_point = vsub(volcano, offset)
    left_point = vadd(volcano, (offset[1], -offset[0]))
    right_point = vadd(volcano, (-offset[1], offset[0]))

    down_slice = tuple(c for c in bresenham(volcano, opposite_point) if c in grid)
    left_slice = tuple(c for c in bresenham(volcano, left_point) if c in grid)
    right_slice = tuple(c for c in bresenham(volcano, right_point) if c in grid)

    if verbose:
        print('line segments:')
        print_2d('.', grid, {k: '<' for k in left_slice}, {k: 'v' for k in down_slice}, {k:'>' for k in right_slice})

    volcano_cost = {k: int(v) for k, v in grid.items() if v.isnumeric()}
    volcano_cost[start] = 0

    radius = 0
    impassable = {}

    while True:
        if verbose:
            print(f'working on radius {radius}')
        lowest_cost = INF
        shortest_path = None

        for a in down_slice:
            if a in impassable:
                continue

            result = wbfs(start, a, get_neighbors, volcano_cost, right_slice)
            if result is None:
                continue
            cost_to_a, path_to_a = result

            result = wbfs(a, start, get_neighbors, volcano_cost, left_slice)
            if result is None:
                continue
            cost_to_start, path_to_start = result
            total_cost = cost_to_a + cost_to_start
            whole_path = path_to_a + path_to_start

            if total_cost < lowest_cost:
                lowest_cost = total_cost
                shortest_path = whole_path

        if lowest_cost != INF:
            if verbose:
                print(f'shortest path at volcano radius {radius}:')
                print_2d('.',volcano_cost, {k: '-' for k in shortest_path} )

            last_radius = radius
            radius = lowest_cost // 30
            if radius == last_radius:
                if verbose:
                    print(f'found valid path of cost {lowest_cost} at radius {radius}!')
                return radius * lowest_cost
            else:
                if verbose:
                    print(f'shortest path cost {lowest_cost} so increased next radius to {radius}')

            impassable = get_cells(volcano, radius)
            for c in impassable:
                volcano_cost.pop(c, None)
        else:
            print(f'could not find path at radius {radius}')
            return -1


setquest(17)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
