import copy

from ec import *


def parse_puzzle(n):
    plants = {}
    test_cases = None

    data = parse_double_break(n)
    for plant in data:
        split = plant.split('\n')
        if not split[0].startswith('Plant'):
            test_cases = tuple(get_ints(line) for line in split if line != '')
        else:
            id, thickness = get_ints(split[0])
            plants[id] = {'t': thickness, 'i': deque(), 'o': [], 'e': 0}
            for branch in split[1:]:
                ints = get_ints(branch)
                if len(ints) == 1:
                    plants[id]['e'] = ints[0]
                else:
                    plants[id]['i'].append(ints)
                    plants[ints[0]]['o'].append([id, ints[1]])
    return plants, test_cases


def run_sim(p_copy):
    while True:
        for k, v in p_copy.items():
            incoming = v['i']
            for i in range(len(incoming)):
                thing = incoming.popleft()
                other_plant_id, thickness = thing
                other_plant = p_copy[other_plant_id]
                if len(other_plant['i']) == 0:
                    p_copy[k]['e'] += thickness * other_plant['e']
                else:
                    incoming.append(thing)

            if len(incoming) == 0 and v['e'] < v['t']:
                v['e'] = 0

        if all(len(x['i']) == 0 for x in p_copy.values()):
            return p_copy[max(p_copy)]['e']


def p1():
    plants, test_cases = parse_puzzle(1)
    return run_sim(plants)


def p2():
    plants, test_cases = parse_puzzle(2)

    acc = 0
    for test_case in test_cases:
        p_copy = copy.deepcopy(plants)
        for i, v in enumerate(test_case):
            p_copy[i + 1]['e'] = v
        acc += run_sim(p_copy)
    return acc


def p3():
    plants, test_cases = parse_puzzle(3)

    bad_starting_plants = set()
    for k, v in plants.items():
        if len(v['i']) != 0:
            continue
        if all(out[1] < 0 for out in v['o']):
            bad_starting_plants.add(k)

    max_state = copy.deepcopy(plants)
    for plant in bad_starting_plants:
        max_state[plant]['e'] = 0

    max_v = run_sim(max_state)

    acc = 0
    for test_case in test_cases:
        p_copy = copy.deepcopy(plants)
        for i, v in enumerate(test_case):
            p_copy[i + 1]['e'] = v
        r = run_sim(p_copy)
        if r == 0:
            continue
        acc += max_v - r

    return acc


setquest(18)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
