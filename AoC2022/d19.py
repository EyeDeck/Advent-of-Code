import heapq
import sys
import re
from collections import *
from operator import itemgetter

robots = {
    'bot_geode': 'geode',
    'bot_obsidian': 'obsidian',
    'bot_clay': 'clay',
    'bot_ore': 'ore',
}


def producible(inv, costs):
    options = {}
    for robot, cost in costs.items():
        cost_o, cost_c, cost_b = cost
        if inv['ore'] >= cost_o and inv['clay'] >= cost_c and inv['obsidian'] >= cost_b:
            options[robot] = cost
    # print('i', inv, 'c', costs, 'opt', options)
    return options


def get_weight_heur(inv):
    return -sum(
        [
            # 1 * inv['ore'],
            1 * inv['bot_ore'],
            # 3 * inv['clay'],
            20 * inv['bot_clay'],
            # 5 * inv['obsidian'],
            200 * inv['bot_obsidian'],
            500 * inv['geode'],
            10000 * inv['bot_geode'],
        ]
    )


def find_paths(inv, costs, minutes, s):
    paths = []
    heapq.heappush(paths, [0, 0, inv])
    seen = set()

    most_ore = max(costs.values(), key=itemgetter(0))[0]
    most_clay = costs['bot_obsidian'][1]
    most_obsidian = costs['bot_geode'][2]

    all_keys = tuple(r for r in robots.keys()) + tuple(r for r in robots.values())

    heap_id = 0

    for minute in range(minutes):
        print(f'{s}: {minute + 1}/{minutes}, paths: {len(paths)}', end='\r')
        new_paths = []

        while paths:
            _, _, inv = heapq.heappop(paths)

            options = producible(inv, costs)

            for robot, product in robots.items():
                if robot in inv:
                    inv[product] += inv[robot]

            # if we can make a geode bot, only do that
            if 'bot_geode' in options:
                options = {'bot_geode': options['bot_geode']}
            else:
                heap_id -= 1
                heapq.heappush(new_paths, [get_weight_heur(inv), heap_id, inv])

            if options:
                for robot, cost in options.items():

                    next_inv = inv.copy()

                    next_inv['ore'] -= cost[0]
                    next_inv['clay'] -= cost[1]
                    next_inv['obsidian'] -= cost[2]

                    next_bot_ct = next_inv[robot] + 1
                    next_inv[robot] = next_bot_ct

                    if robot == 'bot_ore':  # ore robot
                        # don't produce more than any robot uses
                        if next_bot_ct > most_ore:
                            continue
                    elif robot == 'bot_clay':  # clay robot
                        # don't produce more than obsidian robot uses
                        if next_bot_ct > most_clay:
                            continue
                    elif robot == 'bot_obsidian':  # obsidian robot
                        # don't produce more than geode robot uses
                        if next_bot_ct > most_obsidian:
                            continue

                    hashable = tuple(next_inv[k] for k in all_keys)
                    if hashable in seen:
                        continue
                    seen.add(hashable)

                    heap_id -= 1
                    heapq.heappush(new_paths, [get_weight_heur(next_inv), heap_id, next_inv])
        for _ in range(min(len(new_paths), 1000)):
            heapq.heappush(paths, heapq.heappop(new_paths))
    print(' ' * 50, end='\r')
    return max(paths, key=lambda x: x[2]['geode'])[2]['geode']


def p1():
    acc = 0
    for i, cost in enumerate(costs):
        start_inv = defaultdict(int)
        start_inv['bot_ore'] = 1

        acc += (i + 1) * find_paths(start_inv, cost, 24, f'part 1: {i + 1}/{len(data) + 1}')
    return acc


def p2():
    acc = 1
    for i, cost in enumerate(costs[:3]):
        start_inv = defaultdict(int)
        start_inv['bot_ore'] = 1

        n = find_paths(start_inv, cost, 32, f'part 2: {i + 1}/3')
        acc *= n
    return acc


day = 19
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(i) for i in re.findall(r'[0-9]+', line)][1:] for line in file]

costs = []
for bp in data:
    costs.append({'bot_ore': (bp[0], 0, 0), 'bot_clay': (bp[1], 0, 0), 'bot_obsidian': (bp[2], bp[3], 0), 'bot_geode': (bp[4], 0, bp[5])})

print('part1:', p1())
print('part2:', p2())
