import copy
import heapq
import re
import sys
from collections import *


def try_add(d, curr, open, pressure):
    key = (curr, open)
    if key not in d or d[key] < pressure:
        d[key] = pressure


def p1():
    sims = {('AA', frozenset()): 0}
    # print(sims)
    for minute in range(30):
        next_sims = {}
        for (curr, open), pressure in sims.items():
            pressure += sum([valves[o]['i'] for o in open])

            # print(f'minute {minute} @ {curr} w/ {open}, p={pressure}')

            if valves[curr]['i'] > 0 and curr not in open:
                nxt = frozenset([k for k in open] + [curr])
                try_add(next_sims, curr, nxt, pressure)

            neighbors = valves[curr]['n']
            for n in neighbors:
                try_add(next_sims, n, open, pressure)

            # print(neighbors)

        sims = next_sims
    return max(v for v in sims.values())


def p2():
    def try_add(d, me, elephant, open, pressure):
        k1 = (me, elephant)
        k2 = open
        if k1 not in d:
            d[k1] = defaultdict(int)
        if d[k1][k2] < pressure:
            d[k1][k2] = pressure

    sims = {('AA', 'AA'): {frozenset(): 0}}
    # print(sims)
    for minute in range(26):
        print(f'minute {minute} ({len(sims)})...', end='\r')
        next_sims = {}
        for (me, el), all_open in sorted(sims.items()):
            for open, pressure in all_open.items():
                # print(me, el, open)
                pressure += sum([valves[o]['i'] for o in open])

                # print(f'minute {minute} @ {me} {el} w/ {open}, p={pressure}')

                comb_sims = set()
                for my_action, e_action in [[True, True], [False, True], [True, False], [False, False]]:
                    # print(my_action, e_action)
                    my_sims = []
                    el_sims = []
                    if my_action:  # open
                        if valves[me]['i'] > 0 and me not in open:
                            my_open = me
                            my_sims.append([me, el, [me]])
                    else:
                        for neighbor in valves[me]['n']:
                            my_sims.append([neighbor, el, []])

                    if e_action:  # open
                        if valves[el]['i'] > 0 and el not in open:
                            el_sims.append([me, el, [el]])
                    else:  # movement
                        for neighbor in valves[el]['n']:
                            el_sims.append([me, neighbor, []])

                    for sim1 in my_sims:
                        for sim2 in el_sims:
                            for a in [sim1, sim2]:
                                for b in [sim1, sim2]:
                                    comb_sims.add((a[0], b[1], frozenset(list(open) + list(sim1[2]) + list(sim2[2]))))
                    comb_sims.add((me, el, open))
                    # print(sorted(comb_sims))
                for new_sim in comb_sims:
                    try_add(next_sims, *new_sim, pressure)

        # print(next_sims)

        sims = next_sims
        s_size = 0

        for (my_pos, e_pos), open in copy.deepcopy(next_sims).items():
            for opens_a, v_a in open.items():
                s_size += len(opens_a)
                for opens_b, v_b in open.items():
                    if opens_a == opens_b:
                        continue
                    if opens_a <= opens_b and v_a < v_b:
                        try:
                            del sims[(my_pos, e_pos)][opens_a]
                        except KeyError:
                            pass
        best_sims = []
        for (my_pos, e_pos), open in copy.deepcopy(next_sims).items():
            for opens, v in open.items():
                # print((my_pos, e_pos), opens, v)
                heapq.heappush(best_sims, [-v, (my_pos, e_pos), opens])
            # print(my_pos, e_pos, open)
        # print(s_size)
        # print(best_sims)

        sims = defaultdict(defaultdict)
        for i in range(min(1000, len(best_sims))):
            v, (me, el), open = heapq.heappop(best_sims)
            # print('aaa', (me, el), open, v)
            sims[(me, el)][open] = -v
        # print('sims', sims)

        # input()
    print(' ' * 50, end='\r')

    m = 0
    for sim in sims.items():
        # print(sim)
        for open, v in sim[1].items():
            m = max(m, v)
    return m
    # return max(v for v in sims.values())


day = 16
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [re.findall(r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnel[s]? lead[s]? to valve[s]? (.*)', line)[0] for
            line in file]
    valves = defaultdict(dict)
    for line in data:
        valve = line[0]
        valves[valve]['i'] = int(line[1])
        valves[valve]['n'] = set(line[2].split(', '))

print('part1:', p1())
print('part2:', p2())
