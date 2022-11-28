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

f = 'd14e.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

lines = open(f).readlines()
reactants_raw = [[m.strip().split(' ') for m in re.findall(('([\d]+ \w+)'), line)] for line in lines]
reactants = {v[-1][1]: (int(v[-1][0]), {w[1]: int(w[0]) for w in v[:-1]}) for v in reactants_raw}

sys.setrecursionlimit(100000)
print('p1:', ore_amt('FUEL', 1, defaultdict(int)))

p2 = 0
for i in range(63, -1, -1):
    nums = [p2, p2 + (1 << i)]
    cts = [0, 0]
    for j in range(2):
        cts[j] = 1000000000000 - ore_amt('FUEL', nums[j], defaultdict(int))
    best = 1 if 0 < cts[1] < cts[0] else 0
    new = nums[best]
    #if new != p2:
    #    print(nums, [bin(n) for n in nums])
    p2 = new
    print(p2, bin(p2), cts[best])
print('p2:', p2)
