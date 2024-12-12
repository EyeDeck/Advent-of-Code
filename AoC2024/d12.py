import copy
from aoc import *


def p1():
    unprocessed = copy.deepcopy(grid)
    plots_with_id = {}
    id = 0
    while unprocessed:
        # print(unprocessed)
        k,v = unprocessed.popitem()
        flooded = set()
        frontier = deque([k])
        while frontier:
            point = frontier.popleft()
            if point in unprocessed:
                del unprocessed[point]
            flooded.add(point)
            neighbors = [vadd(point, dir) for dir in DIRS]
            for neighbor in neighbors:
                if neighbor not in grid or neighbor in flooded or neighbor in frontier:
                    continue
                if grid[neighbor] == v:
                    frontier.append(neighbor)
        plots_with_id[id] = flooded
        id += 1
    print(plots_with_id)

    grid_separated = {}
    for k,v in plots_with_id.items():
        for point in v:
            grid_separated[point] = k

    print(grid_separated)

    areas = {k:len(v) for k,v in plots_with_id.items()}
    perimeters = defaultdict(int)
    for plot, points in plots_with_id.items():
        print(plot, points)
        for point in points:
            neighbors = [vadd(point, dir) for dir in DIRS]
            for neighbor in neighbors:
                # todo: 'neighbor in frontier' O(n), needs fixing
                if neighbor not in grid_separated or grid_separated[neighbor] != plot:
                    perimeters[plot] += 1
    print(areas)
    print(perimeters)
    return sum(areas[a]*perimeters[p] for a,p in zip(areas.keys(), perimeters.keys()))


def p2():
    unprocessed = copy.deepcopy(grid)
    plots_with_id = {}
    id = 0
    while unprocessed:
        # print(unprocessed)
        k,v = unprocessed.popitem()
        flooded = set()
        frontier = deque([k])
        while frontier:
            point = frontier.popleft()
            if point in unprocessed:
                del unprocessed[point]
            flooded.add(point)
            neighbors = [vadd(point, dir) for dir in DIRS]
            for neighbor in neighbors:
                if neighbor not in grid or neighbor in flooded or neighbor in frontier:
                    continue
                if grid[neighbor] == v:
                    frontier.append(neighbor)
        plots_with_id[id] = flooded
        id += 1
    print(plots_with_id)

    grid_separated = {}
    for k,v in plots_with_id.items():
        for point in v:
            grid_separated[point] = k

    # print(grid_separated)

    areas = {k:len(v) for k,v in plots_with_id.items()}
    perimeters = defaultdict(set)
    for plot, points in plots_with_id.items():
        print(plot, points)
        for point in points:
            neighbors = [(vadd(point, dir), dir) for dir in DIRS]
            for neighbor, dir in neighbors:
                if neighbor not in grid_separated or grid_separated[neighbor] != plot:
                    perimeters[plot].add((point, dir))
    # print(areas)
    # print(perimeters)
    # die()

    merged_fences = {}
    for plot, fence_segments in perimeters.items():
        # print(plot, fence_segments)
        fences = defaultdict(set)
        fence_id = 0
        while fence_segments:
            frontier = deque([fence_segments.pop()])
            while frontier:
                point, dir = frontier.popleft()
                n_dir = (dir[1], dir[0])
                fences[fence_id].add((point, dir))
                neighbors = [vadd(point, n_dir), vsub(point, n_dir)]
                for neighbor in neighbors:
                    neighbor = (neighbor, dir)
                    # print('neighbor', neighbor, 'fs', fence_segments)
                    if neighbor in fence_segments:
                        fence_segments.remove(neighbor)
                        frontier.append(neighbor)
            fence_id += 1
        merged_fences[plot] = fences
        # print('fences', plot, fences)

    # print()
    # print(merged_fences)
    return sum(areas[a]*len(merged_fences[p]) for a,p in zip(areas.keys(), merged_fences.keys()))


setday(12)

grid, inverse, unique = parsegrid()

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1() )
print('part2:', p2() )
