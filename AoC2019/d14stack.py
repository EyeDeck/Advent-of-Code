import math
import re
import sys
from collections import defaultdict


def ore_amt(target, amt, surplus):
    if target == 'ORE':
        return amt

    if surplus[target] > amt:
        surplus[target] -= amt
        return 0

    amt -= surplus[target]
    del surplus[target]

    produced, ingredients = reactants[target]
    to_produce = math.ceil(amt / produced)
    # print(amt, produced, to_produce)

    out = 0
    for r, v in ingredients.items():
        v *= to_produce
        out += ore_amt(r, v, surplus)

    local_surplus = produced * to_produce - amt
    if local_surplus > 0:
        surplus[target] += local_surplus

    return out


def calc_ore_for(initial_ingredient, initial_count):
    stack = [(initial_ingredient, initial_count)]
    surplus = defaultdict(int)
    ore = 0
    while len(stack):
        print('surplus:', surplus)
        for thing in stack:
            cur, needed = thing
            if cur == 'ORE':
                surplused = surplus[cur]
                if surplused > needed:
                    surplus[cur] -= needed
                else:
                    ore += needed
                continue

            created, ingredients = reactants[cur]
            print(cur, needed, created, ingredients)
            for ing, req in ingredients.items():
                # if ing == 'ORE':
                #    # ore_needed = surplus['ORE']
                #    ore += req
                #    continue
                surplused = surplus[ing]
                print('surplused', surplused)
                if surplused < req:
                    # surplus[ing] += req
                    stack.append((ing, req))
    return 0


f = 'd14e.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

lines = open(f).readlines()
reactants_raw = [[m.strip().split(' ') for m in re.findall(('([\d]+ \w+)'), line)] for line in lines]
reactants = {v[-1][1]: (int(v[-1][0]), {w[1]: int(w[0]) for w in v[:-1]}) for v in reactants_raw}
print(reactants, '\n')

print(calc_ore_for('FUEL', 1))

# print('p1:', ore_amt('FUEL', 1, defaultdict(int)))
#
# p2 = 0
# for i in range(63, -1, -1):
#     nums = [p2, p2 + (1 << i)]
#     cts = [0, 0]
#     for j in range(2):
#         cts[j] = 1000000000000 - ore_amt('FUEL', nums[j], defaultdict(int))
#     new = nums[1] if 0 < cts[1] < cts[0] else nums[0]
#     if new != p2:
#         print(nums, [bin(n) for n in nums])
#     p2 = new
# print('p2:', p2)
