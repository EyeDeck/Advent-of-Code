import copy
import itertools
from aoc import *



def solve(p2):
    if p2:
        data[0] += 'elerium generator, elerium-compatible microchip, dilithium generator, dilithium-compatible microchip'

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

    cur = copy.deepcopy(floors)
    cur['floor'] = 0
    cur['min'] = 0

    q = []
    heapq.heappush(q, [0, 0, 0, cur])
    print(q)

    seen = {}
    parent = {0: [None, cur]}

    i = 0
    while q:
        if i % 10000 == 0:
            print(len(seen), len(q))
        # steps, cur = q.popleft()
        score, steps, q_id, cur = heapq.heappop(q)
        # print(f'popped {score}, {steps}, {q_id}, \n{cur}')

        if cur['min'] == 3:
            print(steps, cur)

            thing = q_id
            while thing is not None:
                thing, node = parent[thing]
                print(node, thing)

            return steps

        neighbors = []

        def is_valid(state, floors_to_check):
            # if len(next_state[next_floor]['gens']) > 0:
            #     invalid = False
            #     for chip in next_state[next_floor]['chips']:
            #         if chip not in next_state[next_floor]['gens']:
            #             invalid = True
            #             break
            #     if invalid:
            #         continue

            # print('input state:\n', state)
            for f in floors_to_check:
                f_gens = state[f]['gens']
                f_chips = state[f]['chips']
                for chip in f_chips:
                    if chip in f_gens:
                        continue
                    elif len(f_gens) > 0:
                        # print('invalid', state)
                        # input()
                        return False
                # f_gens = state[f]['gens'].copy()
                # f_chips = state[f]['chips'].copy()
                # # print(f_gens, f_chips, '/', next_state[f]['gens'], next_state[f]['chips'])
                # for chip in f_chips.copy():
                #     if chip in f_gens:
                #         f_chips.remove(chip)
                #         f_gens.remove(chip)
                # # print(f_gens, f_chips, '/', next_state[f]['gens'], next_state[f]['chips'])
                # if len(f_chips) > 0 and len(f_gens) > 0:
                #     # print('invalid? on floor', f, '\n', state, '\n', '->', f_gens, f_chips)
                #     return False
                #     # input()
            # print('valid?\n')
            # print(next_state[floor]['gens'], next_state[floor]['chips'], '/', f_gens, f_chips)
            # input()
            # print('valid', state)
            return True

        def get_neighbors(state):
            cur_floor = state['floor']

            adj_floors = [f for f in [cur_floor - 1, cur_floor + 1] if state['min'] <= f <= 3]

            # print(floor, steps, adj_floors)

            cur_gens = state[cur_floor]['gens']
            cur_chips = state[cur_floor]['chips']

            combs = [
                *itertools.combinations([('gen', g) for g in cur_gens] + [('chip', c) for c in cur_chips] + [None], 2)]
            # print(combs)

            for next_floor in adj_floors:
                for things_to_take in combs:
                    # if next_floor > cur_floor and None in things_to_take:
                    #     continue

                    next_state = copy.deepcopy(state)
                    next_state['floor'] = next_floor

                    for thing in things_to_take:
                        if thing is None:
                            continue
                        elif thing[0] == 'chip':
                            next_state[cur_floor]['chips'].remove(thing[1])
                            next_state[next_floor]['chips'].append(thing[1])
                            next_state[next_floor]['chips'].sort()
                        elif thing[0] == 'gen':
                            next_state[cur_floor]['gens'].remove(thing[1])
                            next_state[next_floor]['gens'].append(thing[1])
                            next_state[next_floor]['gens'].sort()

                    if not is_valid(next_state, [cur_floor, next_floor]):
                        continue
                    # input()

                    yield next_state

        next_steps = steps + 1

        for next_state in get_neighbors(cur):
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

            # trial and error heuristic, I don't really know why it works at all
            heapq.heappush(q, [(next_steps-5) * score, next_steps, i, n])

            parent[i] = [q_id, n]
            # print(q[-1])

        # input()

    return None


def p2():
    return None


setday(11)

data = parselines()

print('part1:', solve(False) )
print('part2:', solve(True) )