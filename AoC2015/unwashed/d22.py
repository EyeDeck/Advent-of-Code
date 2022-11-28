import copy
import sys
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
from collections import *
from math import *
from pprint import pprint

from aoc import *


# INF = 999999999
# mkmat(sx, sy, val=0)
# fw(m)
# get0()
# get1(cvt=str)
# get2(cvt=str)
# @memo
# splat(f)
# bfs(src, tgt, {n1: [n2, n3, n4]})
# wbfs(src, tgt, edge_func)
# astar(src, tgt, edge_func, heur_func)
# ccs(srcs, neigh_func, filt_func?)
# Dedup().seen(x)
# mkcls('Name', f1=v1, f2=v2, ...)
# print_2d(padding, *dicts, constrain=(-256, -256, 256, 256)):
# print_2d_repl(padding, *dicts, constrain=(-256, -256, 256, 256)):

dbg = True
# dbg = False

def get_available(state):
    available = []
    mana = state['player']['mana']

    for spell, stats in spells.items():
        if mana < stats[0]:
            continue
        if stats[1] == 0 or spell not in state['active_effects']:
            available.append((spell,) + stats)
    return available

if dbg:
    def get_available(state):
        spell = test_thing.pop(0)
        stats = spells[spell]
        return [(spell,) + stats]


# def tick_effects(state):
#     effects = state['active_effects']
#     # print(effects)
#
#     if 'Shield' in effects:
#         if effects['Shield'] <= 0:
#             del effects['Shield']
#             state['player']['defense'] = 0
#         else:
#             state['player']['defense'] = 7
#             effects['Shield'] -= 1
#
#     if 'Poison' in effects:
#         if effects['Poison'] <= 0:
#             del effects['Poison']
#         else:
#             state['boss']['hp'] -= 3
#             effects['Poison'] -= 1
#
#     if 'Recharge' in effects:
#         if effects['Recharge'] <= 0:
#             del effects['Recharge']
#         else:
#             state['player']['mana'] += 101
#             effects['Recharge'] -= 1



def tick_effects(state):
    effects = state['active_effects']
    # print(effects)

    if 'Shield' in effects:
        state['player']['defense'] = 7
        if dbg:
            print('shield applies to player (+7)')
        effects['Shield'] -= 1
        if effects['Shield'] <= 0:
            if dbg:
                print('shield effect ended')
            del effects['Shield']

    if 'Poison' in effects:
        state['boss']['hp'] -= 3
        if dbg:
            print('poison damaged boss (-3)')
        effects['Poison'] -= 1
        if effects['Poison'] <= 0:
            if dbg:
                print('poison effect ended')
            del effects['Poison']

    if 'Recharge' in effects:
        state['player']['mana'] += 101
        if dbg:
            print('player recharged mana (+101)')
        effects['Recharge'] -= 1
        if effects['Recharge'] <= 0:
            if dbg:
                print('recharge effect ended')
            del effects['Recharge']


def check_end(state):
    if state['player']['hp'] <= 0 or state['player']['mana'] <= 0:
        if dbg:
            print('player died', state)
        return True, False
    elif state['boss']['hp'] <= 0:
        if dbg:
            print('player wins!', state)
        return True, True
    else:
        return False, False


def tick_boss(state):
    if state['boss']['skip']:
        if dbg:
            print('skipped turn')
        state['boss']['skip'] = False
    else:
        dmg = max(1, state['boss']['damage'] - state['player']['defense'])
        if dbg:
            print('boss hits player for', dmg)
        state['player']['hp'] -= dmg
        # print('took', dmg)

    return check_end(state)


def tick_player(state, spell):
    name, mana_cost, turns = spell
    state['history'].append(name)
    state['player']['mana'] -= mana_cost
    state['player']['spent'] += mana_cost
    if dbg:
        print('player casts', name, 'for', mana_cost)
    if name == 'Magic Missile':
        state['boss']['hp'] -= 4
        if dbg:
            print('player hits boss for 4')
    elif name == 'Drain':
        state['boss']['hp'] -= 2
        state['player']['hp'] += 2
        if dbg:
            print('player hits boss for 2 and heals 2')
    else:
        state['active_effects'][name] = turns
        if dbg:
            print('player starts', name, 'for', turns, 'turns')

    return check_end(state)


def p1():
    state = {
        'player': {
            'hp': 50,
            'mana': 500,
            'defense': 0,
            'spent': 0,
        },
        'boss': {
            'hp': boss['hp'],
            'damage': boss['damage'],
            'skip': True,
        },
        'active_effects': {},
        'history': []
    }
    active = deque([state])
    winning_states = []
    best = INF
    while active:
        # cur = active.popleft()
        cur = active.pop()
        # input()

        # boss turn
        if dbg:
            print('---boss\'s turn started---')
        tick_effects(cur)

        ended, won = check_end(cur)
        if won:
            # winning_states.append(cur)
            spent = cur['player']['spent']
            # print(best, spent)
            if spent < best:
                best = spent
                print(cur)
        if ended:
            continue

        ended, won = tick_boss(cur)
        if won:
            # winning_states.append(cur)
            spent = cur['player']['spent']
            # print(best, spent)
            if spent < best:
                best = spent
                print(cur)
        if ended:
            continue

        if dbg:
            print('end of boss:\n', cur)

        cur['player']['defense'] = 0
        # print(best)

        # player turn
        if dbg:
            print('---player\'s turn started---')
        ended, won = check_end(cur)
        if won:
            # winning_states.append(cur)
            spent = cur['player']['spent']
            if spent < best:
                best = spent
                print(cur)
        if ended:
            continue

        available = get_available(cur)

        for spell in available:
            nxt = copy.deepcopy(cur)

            ended, won = tick_player(nxt, spell)

            if won:
                # winning_states.append(nxt)
                spent = nxt['player']['spent']
                if spent < best:
                    best = spent
                    print(nxt)
            if ended:
                continue

            # print(nxt)
            # input()
            nxt['player']['defense'] = 0
            if dbg:
                print('end of player:\n', nxt)
            active.append(nxt)

        # print(available)
    # print(winning_states)
    return None


def p2():
    return None


day = 22
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    f = [[word for word in line.split()] for line in file.read().split('\n')]
    boss = {'hp': int(f[0][-1]), 'damage': int(f[1][-1])}
print(boss)

spells = {
    'Magic Missile': (53, 0),
    'Drain': (73, 0),
    'Shield': (113, 6),
    'Poison': (173, 6),
    'Recharge': (229, 5)
}

# test_thing = ['Recharge', 'Poison', 'Shield', 'Magic Missile', 'Magic Missile', 'Poison', 'Shield', 'Magic Missile', 'Magic Missile', 'Magic Missile', 'Magic Missile']
# test_thing = ['Recharge', 'Poison', 'Shield', 'Recharge', 'Poison', 'Shield', 'Magic Missile', 'Poison', 'Magic Missile', 'Magic Missile']
# test_thing = ['Recharge', 'Poison', 'Shield', 'Recharge', 'Poison', 'Shield', 'Magic Missile', 'Poison', 'Magic Missile', 'Magic Missile']
test_thing = ['Recharge', 'Poison', 'Shield', 'Magic Missile', 'Magic Missile', 'Recharge', 'Magic Missile', 'Magic Missile', 'Shield', 'Magic Missile', 'Magic Missile', 'Magic Missile', 'Magic Missile', 'Magic Missile', 'Magic Missile']
# print(sum([spells[s][0] for s in test_thing]))

print(f'part1: {p1()}')  # 1139 too low, 1186 too low, 1415 wrong, 1362 wrong, 1342 wrong, 1387 wrong
print(f'part2: {p2()}')
