from ec import *
import networkx as nx


def make_graph(grid):
    G = nx.DiGraph()
    for c,v in grid.items():
        G.add_node(c)
        for d in DIRS:
            n = vadd(c,d)
            if n not in grid:
                continue
            nv = grid[n]
            if v >= nv:
                G.add_edge(c,n)
    return G


def p1():
    grid, inverse, unique = parse_grid(1)
    graph = make_graph(grid)
    return len(nx.descendants(graph,(0,0))) + 1


def p2():
    grid, inverse, unique = parse_grid(2)
    bounds = grid_bounds(grid)
    graph = make_graph(grid)
    points = [(0,0), bounds[2:]]
    running = set()
    for point in points:
        running |= set(nx.descendants(graph,point))
        running.add(point)
    return len(running)


def p3():
    grid, inverse, unique = parse_grid(3)

    acc = 0
    for loop in range(3):
        graph = make_graph(grid)
        points_to_bother_testing = set(grid.keys())
        best_ct = 0
        best_r = None
        while points_to_bother_testing:
            point = points_to_bother_testing.pop()
            r = set(nx.descendants(graph,point))
            r.add(point)
            ct = len(r)
            if ct > best_ct:
                best_ct = ct
                best_r = r
            # any point part of a previous test is necessarily a subset of that previous test, so skip all of them
            points_to_bother_testing -= set(r)
        grid = {k: v for k, v in grid.items() if k not in best_r}
        acc += best_ct

    return acc


setquest(12)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
