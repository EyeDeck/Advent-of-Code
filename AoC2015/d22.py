import copy
import heapq
import sys


def get_available(state):
    if do_fixed:
        spell = trial.pop(0)
        stats = spells[spell]
        return [(spell,) + stats]
    else:
        available = []
        mana = state['player']['mana']

        for spell, stats in spells.items():
            if mana < stats[0]:
                continue
            if stats[1] == 0 or spell not in state['active_effects']:
                available.append((spell,) + stats)
        return available


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
    return check_end(state)


def tick_player(state, spell):
    name, mana_cost, turns = spell
    state['player']['mana'] -= mana_cost
    state['player']['spent'] += mana_cost
    if dbg:
        print('player casts', name, 'for', mana_cost)
        state['history'].append(name)
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


def solve(p2=False):
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
    active = []
    n = 0
    heapq.heappush(active, (state['player']['spent'], state['boss']['hp'], n, state))

    while active:
        _, _, _, cur = heapq.heappop(active)

        # boss turn
        if dbg:
            print('---boss\'s turn started---')
        tick_effects(cur)

        ended, won = check_end(cur)
        if won:
            return cur['player']['spent']
        if ended:
            continue

        ended, won = tick_boss(cur)
        if won:
            return cur['player']['spent']
        if ended:
            continue

        if dbg:
            print('end of boss:\n', cur)

        cur['player']['defense'] = 0

        # player turn
        if p2:
            cur['player']['hp'] -= 1
        if dbg:
            print('---player\'s turn started---')
        tick_effects(cur)
        ended, won = check_end(cur)
        if won:
            return cur['player']['spent']
        if ended:
            continue

        available = get_available(cur)

        for spell in available:
            nxt = copy.deepcopy(cur)

            ended, won = tick_player(nxt, spell)

            if won:
                return nxt['player']['spent']
            if ended:
                continue

            nxt['player']['defense'] = 0
            if dbg:
                print('end of player:\n', nxt)
            heapq.heappush(active, (nxt['player']['spent'], nxt['boss']['hp'], n := n + 1, nxt))
    return None


day = 22
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    f = [[word for word in line.split()] for line in file.read().split('\n')]
    boss = {'hp': int(f[0][-1]), 'damage': int(f[1][-1])}
# print(boss)

spells = {
    'Magic Missile': (53, 0),
    'Drain': (73, 0),
    'Shield': (113, 6),
    'Poison': (173, 6),
    'Recharge': (229, 5)
}

dbg = '--debug' in sys.argv
do_fixed = '--test' in sys.argv

# trial = ['Poison', 'Magic Missile', 'Recharge', 'Shield', 'Magic Missile', 'Magic Missile', 'Magic Missile', 'Recharge', 'Magic Missile', 'Shield', 'Magic Missile', 'Magic Missile', 'Magic Missile', 'Magic Missile', 'Magic Missile']
# print(sum([spells[s][0] for s in trial]))

print(f'part1: {solve()}')
print(f'part2: {solve(True)}')
