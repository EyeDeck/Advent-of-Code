import copy
import itertools
from aoc import *



def p1():
    floors = {}
    for i, line in enumerate(data):
        floors[i] = defaultdict(list)
        for object in re.findall("(\w+(?: generator|-compatible microchip))", line):
            l, r = object.split()
            l = l.split('-')[0]
            if r == 'microchip':
                floors[i]['chips'].append(l)
            else:
                floors[i]['gens'].append(l)
    print(floors)

    state = copy.deepcopy(floors)
    state['floor'] = 0
    state['min'] = 0

    q = []
    heapq.heappush(q, [0, 0, 0, state])
    print(q)

    seen = {}

    i = 0
    while q:
        if i % 10000 == 0:
            print(len(seen), len(q))
        # steps, cur = q.popleft()
        score, steps, _, cur = heapq.heappop(q)
        # print('popped', steps, cur)

        if cur['min'] == 3:
            print(steps, cur)
            return steps

        neighbors = []

        floor = cur['floor']

        adj_floors = [f for f in [floor-1, floor+1] if cur['min'] <= f <= 3]

        # print(floor, steps, adj_floors)

        cur_gens = cur[floor]['gens']
        cur_chips = cur[floor]['chips']

        combs = [*itertools.combinations([('gen', g) for g in cur_gens] + [('chip', c) for c in cur_chips] + [None], 2)]
        # print(combs)

        next_steps = steps + 1

        for next_floor in adj_floors:

            for things_to_take in combs:

                # if next_floor < adj_floors and None in things_to_take:
                #     continue

                next_state = copy.deepcopy(cur)
                next_state['floor'] = next_floor

                for thing in things_to_take:
                    if thing is None:
                        continue
                    elif thing[0] == 'chip':
                        next_state[floor]['chips'].remove(thing[1])
                        next_state[next_floor]['chips'].append(thing[1])
                        next_state[next_floor]['chips'].sort()
                    elif thing[0] == 'gen':
                        next_state[floor]['gens'].remove(thing[1])
                        next_state[next_floor]['gens'].append(thing[1])
                        next_state[next_floor]['gens'].sort()

                # if len(next_state[next_floor]['gens']) > 0:
                #     invalid = False
                #     for chip in next_state[next_floor]['chips']:
                #         if chip not in next_state[next_floor]['gens']:
                #             invalid = True
                #             break
                #     if invalid:
                #         continue

                valid = True
                for f in [floor, next_floor]:
                    f_gens = next_state[f]['gens'].copy()
                    f_chips = next_state[f]['chips'].copy()
                    # print(f_gens, f_chips, '/', next_state[f]['gens'], next_state[f]['chips'])
                    for chip in f_chips.copy():
                        if chip in f_gens:
                            f_chips.remove(chip)
                            f_gens.remove(chip)
                    # print(f_gens, f_chips, '/', next_state[f]['gens'], next_state[f]['chips'])
                    if len(f_chips) > 0 and len(f_gens) > 0:
                        # print('invalid? on floor', f, '\n', next_state, '\n', '->', f_gens, f_chips)
                        valid = False
                        # input()
                        break
                if not valid:
                    continue
                # print('valid?', '\n', next_state, '\n')
                    # print(next_state[floor]['gens'], next_state[floor]['chips'], '/', f_gens, f_chips)
                    # input()

                lowest_floor = next_state[next_state['min']]
                if len(lowest_floor['gens']) == 0 and len(lowest_floor['chips']) == 0:
                    # print('inc lowest...')
                    del next_state[next_state['min']]
                    next_state['min'] += 1
                    # print(next_state)

                hashable = str(next_state)
                if hashable in seen and seen[hashable] <= next_steps:
                    # print(seen[hashable], next_steps, 'found better path to', hashable)
                    continue

                seen[hashable] = next_steps

                neighbors.append(next_state)

        # print('\nneighbors:')
        for n in neighbors:
            i += 1
            score = 0
            for floor in range(n['min'], 4):
                # print(floor, n[floor]['gens'], n[floor]['chips'], (3-floor) * (len(n[floor]['gens']) + len(n[floor]['chips'])))
                score += (3-floor) * (len(n[floor]['gens']) + len(n[floor]['chips']))

            # print(n)
            # input()
            # print(score)
            # print('added', n)
            # input()
            heapq.heappush(q, [next_steps * score, next_steps, i, n])
            # print(q[-1])

        # input()

    return None

    # 29 not right...
    # 27 not right


def p2():
    return None


setday(11)

data = parselines()

print('part1:', p1() )
print('part2:', p2() )