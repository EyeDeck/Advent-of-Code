import sys
import itertools
import heapq


def get_costs():
    all_combs = itertools.product(weapons, armors, itertools.combinations(rings.keys(), 2))
    costs_and_stats = []
    for weapon, armor, (ring1, ring2) in all_combs:
        cost = weapons[weapon]['cost'] + armors[armor]['cost'] + rings[ring1]['cost'] + rings[ring2]['cost']
        damage = weapons[weapon]['damage'] + armors[armor]['damage'] + rings[ring1]['damage'] + rings[ring2]['damage']
        defense = weapons[weapon]['armor'] + armors[armor]['armor'] + rings[ring1]['armor'] + rings[ring2]['armor']
        heapq.heappush(costs_and_stats, (cost, damage, defense))
    return costs_and_stats


def p1():
    costs_and_stats = get_costs()
    while costs_and_stats:
        cost, damage, defense = heapq.heappop(costs_and_stats)
        player_hp = 100
        boss_hp = boss['hp']
        while True:
            boss_hp -= max(1, damage - boss['armor'])
            if boss_hp <= 0:
                return cost
            player_hp -= max(1, boss['damage'] - defense)
            if player_hp <= 0:
                break


def p2():
    costs_and_stats = get_costs()
    best = 0
    while costs_and_stats:
        cost, damage, defense = heapq.heappop(costs_and_stats)
        player_hp = 100
        boss_hp = boss['hp']
        while True:
            boss_hp -= max(1, damage - boss['armor'])
            if boss_hp <= 0:
                break
            player_hp -= max(1, boss['damage'] - defense)
            if player_hp <= 0:
                best = max(best, cost)
    return best


day = 21
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    f = [[word for word in line.split()] for line in file.read().split('\n')]
    boss = {'hp': int(f[0][-1]), 'damage': int(f[1][-1]), 'armor': int(f[2][-1])}

weapons_raw = '''
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
'''

armor_raw = '''
Nothing      0      0       0
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
'''

rings_raw = '''
Nothing1      0     0       0
Nothing2      0     0       0
Damage+1     25     1       0
Damage+2     50     2       0
Damage+3    100     3       0
Defense+1    20     0       1
Defense+2    40     0       2
Defense+3    80     0       3
'''

weapons = {}
armors = {}
rings = {}
for unparsed, category in [[weapons_raw, weapons], [armor_raw, armors], [rings_raw, rings]]:
    for line in unparsed.strip().split('\n'):
        sp = line.split()
        category[sp[0]] = {'cost': int(sp[-3]), 'damage': int(sp[-2]), 'armor': int(sp[-1])}
# print(weapons, armors, rings)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
