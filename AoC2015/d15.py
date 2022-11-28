import heapq
import math
import sys


def score(recipe, with_cal=False):
    t = [0 for _ in range(len(map2))]
    for recipe_index, recipe_count in enumerate(recipe):
        for property_index, property_name in map2.items():
            t[property_index] += data[map1[recipe_index]][map2[property_index]] * recipe_count
    t = [max(n, 0) for n in t]
    if with_cal:
        return math.prod(t[:-1]), t[-1]
    else:
        return math.prod(t[:-1])


def solve():
    start = tuple([100//len(data) for _ in range(len(data))])
    active = []
    start_score, start_cal = score(start, True)
    heapq.heappush(active, (-start_score, start_cal, start))
    best = 0
    best_500 = 0
    seen = set()
    while active:
        sc, cal, recipe = heapq.heappop(active)
        if sc < best:
            best = sc
        if sc < best_500 and cal == 500:
            best_500 = sc

        for i in range(len(map1)):
            for j in range(len(map1)):
                if i == j:
                    continue
                new_recipe = list(recipe)
                new_recipe[i] -= 1
                new_recipe[j] += 1
                new_recipe = tuple(new_recipe)
                if new_recipe in seen:
                    continue
                seen.add(new_recipe)
                new_sc, new_cal = score(new_recipe, True)
                if new_sc == 0:
                    continue
                heapq.heappush(active, (-new_sc, new_cal, new_recipe))
    return -best, -best_500


day = 15
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

data = {}
with open(f) as file:
    for line in file:
        k, r = line.split(':')
        data[k] = {(x := k.split())[0]: int(x[1]) for k in r.split(',')}
map1 = {i:k for i,k in enumerate(data.keys())}
map2 = {i:k for i,k in enumerate(data[map1[0]].keys())}

print('part1: %s\npart2: %s' % solve())
