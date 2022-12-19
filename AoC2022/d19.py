import sys
import re
from collections import *
from operator import itemgetter

robots = {
    'g_rb': 'geode',
    'b_rb': 'obsidian',
    'c_rb': 'clay',
    'o_rb': 'ore',
}

# def find_paths(inv, minute, costs):
#     for robot, product in robots.items():
#         # print(robot, product)
#         if robot in inv:
#             # print('added', product, 'from', robot)
#             inv[product] += 1
#
#     if minute == 24:
#         return inv
#
#     options = []
#     for robot, cost in costs.items():
#         if inv['ore'] >= cost[0] and inv['clay'] >= cost[1] and inv['obsidian'] >= cost[2]:
#             options.append([robot, cost])
#     # print(inv, minute) # , options)
#     # input()
#
#     r = [find_paths(inv, minute+1, costs)]
#     if options:
#         for robot, cost in options:
#             next_inv = inv.copy()
#
#             next_inv['ore'] -= cost[0]
#             next_inv['clay'] -= cost[1]
#             next_inv['obsidian'] -= cost[2]
#
#             next_inv[robot] += 1
#
#             r.append(find_paths(next_inv, minute+1, costs))
#
#     return r


# def producible(inv, costs):
#     options = {}
#     for robot, cost in costs.items():
#         cost_o, cost_c, cost_b = cost
#         o = INF if cost_o == 0 else inv['ore'] // cost_o
#         c = INF if cost_c == 0 else inv['clay'] // cost_c
#         b = INF if cost_b == 0 else inv['obsidian'] // cost_b
#         ct = min(o, c, b)
#         if ct > 0:
#             options[robot] = (ct, cost)
#     # print('i', inv, 'c', costs, 'opt', options)
#     return options


def producible(inv, costs):
    options = {}
    for robot, cost in costs.items():
        cost_o, cost_c, cost_b = cost
        if inv['ore'] >= cost_o and inv['clay'] >= cost_c and inv['obsidian'] >= cost_b:
            options[robot] = cost
    # print('i', inv, 'c', costs, 'opt', options)
    return options


def find_paths(inv, costs, minutes, s):
    paths = [inv]
    seen = set()

    most_ore = max(costs.values(), key=itemgetter(0))[0]
    most_clay = costs['b_rb'][1]
    most_obsidian = costs['g_rb'][2]

    all_keys = tuple(r for r in robots.keys()) + tuple(r for r in robots.values())

    # print(most_ore, most_clay, most_obsidian)

    for minute in range(minutes):
        print(f'{s}: {minute+1}/{minutes}, paths: {len(paths)}', end='\r')
        new_paths = []

        while paths:
            inv = paths.pop()

            options = producible(inv, costs)

            for robot, product in robots.items():
                # print(robot, product)
                if robot in inv:
                    # print('added', product, 'from', robot)
                    inv[product] += inv[robot]

            # if inv['geode'] < most_geodes:
            #     continue
            # most_geodes = max(most_geodes, inv['geodes'])

            # print(minute, inv, options)
            # input()

            # if we can make a geode bot, only do that
            if 'g_rb' in options:
                options = {'g_rb': options['g_rb']}
            else:
                new_paths.append(inv)

            if options:
                for robot, cost in options.items():

                    next_inv = inv.copy()

                    next_inv['ore'] -= cost[0]
                    next_inv['clay'] -= cost[1]
                    next_inv['obsidian'] -= cost[2]

                    next_bot_ct = next_inv[robot] + 1
                    next_inv[robot] = next_bot_ct

                    if robot == 'o_rb':  # ore robot
                        # don't produce more than any robot uses
                        if next_bot_ct > most_ore:
                            continue
                    elif robot == 'c_rb':  # clay robot
                        # don't produce more than obsidian robot uses
                        if next_bot_ct > most_clay:
                            continue
                    elif robot == 'b_rb':  # obsidian robot
                        # don't produce more than geode robot uses
                        if next_bot_ct > most_obsidian:
                            continue

                    hashable = tuple(next_inv[k] for k in all_keys)
                    if hashable in seen:
                        continue
                    seen.add(hashable)

                    # if robot == 'g_rb':
                    #     most_geodes = max(next_inv[robot])

                    new_paths.append(next_inv)

        # for path in new_paths:
        #     print(path)
        paths = new_paths
        # input()
    return max(paths, key=itemgetter('geode'))


def p1():
    acc = 0
    for id, bp in enumerate(data):
        costs = {'o_rb': (bp[0], 0, 0), 'c_rb': (bp[1], 0, 0), 'b_rb': (bp[2], bp[3], 0), 'g_rb': (bp[4], 0, bp[5])}
        # print(id, costs)

        start_inv = defaultdict(int)
        start_inv['o_rb'] = 1

        acc += (id+1) * find_paths(start_inv, costs, 24, f'{id+1}/{len(data)+1}')['geode']
        # die()

    return acc


def p2():
    acc = 1
    for id, bp in enumerate(data[:3]):
        costs = {'o_rb': (bp[0], 0, 0), 'c_rb': (bp[1], 0, 0), 'b_rb': (bp[2], bp[3], 0), 'g_rb': (bp[4], 0, bp[5])}
        print(id, costs)

        start_inv = defaultdict(int)
        start_inv['o_rb'] = 1

        acc *= find_paths(start_inv, costs, 32, f'{id + 1}/3')['geode']
        # die()

    return acc


day = 19
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(i) for i in re.findall(r'[0-9]+', line)][1:] for line in file]

# print('part1:', p1())
print('part2:', p2())
