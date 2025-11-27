import copy

from ec import *


def p1():
    plants = {}

    data = parse_double_break(1)
    for plant in data:
        split = plant.split('\n')
        id, thickness = get_ints(split[0])
        # print(id,thickness)
        plants[id] = {'t':thickness, 'i':deque(), 'e':0}
        for branch in split[1:]:
            ints = get_ints(branch)
            if len(ints) == 1:
                plants[id]['e'] = ints[0]
            else:
                plants[id]['i'].append(ints)

    print(plants)
        # for line in plant:

    # print(data)

    while True:
        for k,v in plants.items():
            print(k,v)
            incoming = v['i']
            for i in range(len(incoming)):
                thing = incoming.popleft()
                other_plant_id, thickness = thing
                other_plant = plants[other_plant_id]
                print('popped thing:', thing)
                if len(other_plant['i']) == 0:
                    plants[k]['e'] += thickness * other_plant['e']
                else:
                    incoming.append(thing)

            if len(incoming) == 0 and v['e'] < v['t']:
                v['e'] = 0

        if all(len(x['i']) == 0 for x in plants.values()):
            return plants[max(plants)]['e']

        input()


    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)
    # grid, inverse, unique = parse_grid()

    return


def p2():
    plants = {}
    test_cases = None

    data = parse_double_break(2)
    for plant in data:
        split = plant.split('\n')
        if not split[0].startswith('Plant'):
            test_cases = tuple(get_ints(line) for line in split if line != '')
        else:
            id, thickness = get_ints(split[0])
            # print(id,thickness)
            plants[id] = {'t':thickness, 'i':deque(), 'e':0}
            for branch in split[1:]:
                ints = get_ints(branch)
                if len(ints) == 1:
                    plants[id]['e'] = ints[0]
                else:
                   plants[id]['i'].append(ints)

    print(plants)
    print(test_cases)
    # for line in plant:

    # print(data)
    acc = 0
    for test_case in test_cases:
        p_copy = copy.deepcopy(plants)
        for i, v in enumerate(test_case):
            print(i,v)
            p_copy[i+1]['e'] = v
        while True:
            for k,v in p_copy.items():
                print(k,v)
                incoming = v['i']
                for i in range(len(incoming)):
                    thing = incoming.popleft()
                    other_plant_id, thickness = thing
                    other_plant = p_copy[other_plant_id]
                    print('popped thing:', thing)
                    if len(other_plant['i']) == 0:
                        p_copy[k]['e'] += thickness * other_plant['e']
                    else:
                        incoming.append(thing)

                if len(incoming) == 0 and v['e'] < v['t']:
                    v['e'] = 0

            if all(len(x['i']) == 0 for x in p_copy.values()):
                acc += p_copy[max(p_copy)]['e']
                break
    return acc


def p3():
    plants = {}
    test_cases = None

    data = parse_double_break(3)
    for plant in data:
        split = plant.split('\n')
        if not split[0].startswith('Plant'):
            test_cases = tuple(get_ints(line) for line in split if line != '')
        else:
            id, thickness = get_ints(split[0])
            # print(id,thickness)
            plants[id] = {'t':thickness, 'i':deque(), 'e':0}
            for branch in split[1:]:
                ints = get_ints(branch)
                if len(ints) == 1:
                    plants[id]['e'] = ints[0]
                else:
                   plants[id]['i'].append(ints)

    print(plants)
    # print(test_cases)
    # for line in plant:

    all_starting_plants = {k for k,v in plants.items() if v['e'] != 0}
    # print(starting_plants)
    bad_starting_plants = set()
    for sp in all_starting_plants:
        relevant_plants = [k for k,v in plants.items() if any(i[0] == sp for i in v['i'])]
        # bad = True
        # for plant in plants:
        #     for incoming in plant['i']:
        #         if incoming[0] == sp and incoming[1] > 0:
        #             bad = False
        #             break
        # if not bad:
        print(sp, relevant_plants)
        for rp in relevant_plants:
            rp_i = plants[rp]['i']
            bad = True
            for thing in rp_i:
                if thing[0] != sp:
                    continue
                if thing[1] > 0:
                    bad = False
            if bad:
                bad_starting_plants.add(sp)

    print('bad?', bad_starting_plants)


    max_maybe = copy.deepcopy(plants)
    for plant in bad_starting_plants:
        max_maybe[plant]['e'] = 0

    max_v = run_sim(max_maybe)
    print(max_v)

    # die()

    # print(data)
    acc = 0
    for test_case in test_cases:
        p_copy = copy.deepcopy(plants)
        for i, v in enumerate(test_case):
            # print(i,v)
            p_copy[i+1]['e'] = v
        r = run_sim(p_copy)
        if r == 0:
            continue
        acc += max_v - r

    return acc


def run_sim(p_copy):
    while True:
        for k, v in p_copy.items():
            # print(k,v)
            incoming = v['i']
            for i in range(len(incoming)):
                thing = incoming.popleft()
                other_plant_id, thickness = thing
                other_plant = p_copy[other_plant_id]
                # print('popped thing:', thing)
                if len(other_plant['i']) == 0:
                    p_copy[k]['e'] += thickness * other_plant['e']
                else:
                    incoming.append(thing)

            if len(incoming) == 0 and v['e'] < v['t']:
                v['e'] = 0

        if all(len(x['i']) == 0 for x in p_copy.values()):
            return p_copy[max(p_copy)]['e']


setquest(18)

# print('part1:', p1())
# print('part2:', p2())
print('part3:', p3())
