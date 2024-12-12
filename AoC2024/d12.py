import copy
from aoc import *


def solve():
    # separate each unique plot by picking a random tile and flood filling
    unprocessed = copy.deepcopy(grid)
    plots_with_id = {}
    id = 0
    while unprocessed:
        k, v = unprocessed.popitem()
        flooded = {k}
        frontier = deque([k])
        while frontier:
            point = frontier.popleft()
            if point in unprocessed:
                del unprocessed[point]
            neighbors = [vadd(point, dir) for dir in DIRS]
            for neighbor in neighbors:
                if neighbor not in grid or neighbor in flooded:
                    continue
                if grid[neighbor] == v:
                    frontier.append(neighbor)
                    flooded.add(neighbor)
        plots_with_id[id] = flooded
        id += 1

    # remake a grid, where value is a unique plot ID instead of plant type
    grid_separated = {}
    for k, v in plots_with_id.items():
        for point in v:
            grid_separated[point] = k

    # find all unique fence segments, stored as [plot id] = {(owner tile, owner tile's side), ...}
    perimeters = defaultdict(set)
    for plot, points in plots_with_id.items():
        for point in points:
            neighbors = [(vadd(point, dir), dir) for dir in DIRS]
            for neighbor, dir in neighbors:
                if neighbor not in grid_separated or grid_separated[neighbor] != plot:
                    perimeters[plot].add((point, dir))

    areas = {k: len(v) for k, v in plots_with_id.items()}

    p1 = sum(areas[a] * len(perimeters[p]) for a, p in zip(areas.keys(), perimeters.keys()))

    # merge all connected fence segments
    merged_fences = {}
    for plot, fence_segments in perimeters.items():
        fences = defaultdict(set)
        fence_id = 0
        while fence_segments:
            frontier = deque([fence_segments.pop()])
            while frontier:
                point, dir = frontier.popleft()
                neighbor_dirs = (dir[1], dir[0])
                fences[fence_id].add((point, dir))
                neighbors = [vadd(point, neighbor_dirs), vsub(point, neighbor_dirs)]
                for neighbor in neighbors:
                    neighbor = (neighbor, dir)
                    if neighbor in fence_segments:
                        fence_segments.remove(neighbor)
                        frontier.append(neighbor)
            fence_id += 1
        merged_fences[plot] = fences

    p2 = sum(areas[a] * len(merged_fences[p]) for a, p in zip(areas.keys(), merged_fences.keys()))
    return p1, p2


setday(12)

grid, inverse, unique = parsegrid()

print('part1: %d\npart2: %d' % solve())
