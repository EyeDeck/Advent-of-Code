import math
from aoc import *


def p1():
    modules = {}
    for line in data:
        line = line.split('->')
        kind = line[0][0]
        label = line[0][1 if kind != 'b' else 0:].strip()
        dests = tuple(c.strip() for c in line[1].strip().split(','))
        # print(dests)

        modules[label] = {'state':0, 'type':kind, 'dests':dests}
        if kind == '&':
            modules[label]['inputs'] = {}
        # print(kind, label, dests)
        # print(line)

    # print(modules)

    to_add = []
    for name, module in modules.items():
        for output in module['dests']:
            if output not in modules:
                to_add.append(output)
                continue
            out_module = modules[output]
            if out_module['type'] != '&':
                continue
            out_module['inputs'][name] = 0

    for name in to_add:
        print(name)
        modules[name] = {'state': 0, 'type': '?', 'dests': tuple()}

    print(modules)

    pulses = {0:0, 1:0}

    for i in range(1000):
        stack = deque([('broadcaster', 0, 'button')])
        pulses[0] += 1
        while stack:
            # print(stack)
            label, pulse, sender = stack.popleft()
            module = modules[label]
            dests = module['dests']
            kind = module['type']

            # print(label, pulse, dests, kind)

            if kind == 'b':
                for output in dests:
                    # print(label, '-low->', output)
                    stack.append((output, 0, label))
                    pulses[0] += 1
            elif kind == '%':  # Flip-flop
                if pulse == 1:
                    continue
                module['state'] = module['state'] ^ 1
                to_send = 1 if module['state'] else 0
                for output in dests:
                    pulses[to_send] += 1
                    # print(label, '-low->' if to_send == 0 else '-high->', output)
                    stack.append((output, to_send, label))
            elif kind == '&':  # Conjunction
                module['inputs'][sender] = pulse
                to_send = 0 if sum(module['inputs'].values()) == len(module['inputs']) else 1
                for output in dests:
                    pulses[to_send] += 1
                    # print(label, '-low->' if to_send == 0 else '-high->', output)
                    stack.append((output, to_send, label))

    print(pulses)
    return math.prod(pulses.values())


def p2():
    modules = {}
    for line in data:
        line = line.split('->')
        kind = line[0][0]
        label = line[0][1 if kind != 'b' else 0:].strip()
        dests = tuple(c.strip() for c in line[1].strip().split(','))
        # print(dests)

        modules[label] = {'state':0, 'type':kind, 'dests':dests}
        if kind == '&':
            modules[label]['inputs'] = {}
        # print(kind, label, dests)
        # print(line)

    # print(modules)

    to_add = []
    for name, module in modules.items():
        for output in module['dests']:
            if output not in modules:
                to_add.append(output)
                continue
            out_module = modules[output]
            if out_module['type'] != '&':
                continue
            out_module['inputs'][name] = 0

    for name in to_add:
        print(name)
        modules[name] = {'state': 0, 'type': '?', 'dests': tuple()}

    print(modules)

    pulses = {0:0, 1:0}

    for i in range(1000000000):
        # input()
        # if i % 10000 == 0:
        #     print('\r', i, end='')
        stack = deque([('broadcaster', 0, 'button')])
        pulses[0] += 1
        while stack:
            # print(stack)
            label, pulse, sender = stack.popleft()
            module = modules[label]
            dests = module['dests']
            kind = module['type']

            if label == 'rx' and pulse == 0:
                return i+1

            # print(label, pulse, dests, kind)

            if kind == 'b':
                for output in dests:
                    # print(label, '-low->', output)
                    stack.append((output, 0, label))
                    pulses[0] += 1
            elif kind == '%':  # Flip-flop
                if pulse == 1:
                    continue
                module['state'] = module['state'] ^ 1
                to_send = 1 if module['state'] else 0
                for output in dests:
                    pulses[to_send] += 1
                    # print(label, '-low->' if to_send == 0 else '-high->', output)
                    stack.append((output, to_send, label))
            elif kind == '&':  # Conjunction
                module['inputs'][sender] = pulse
                to_send = 0 if sum(module['inputs'].values()) == len(module['inputs']) else 1
                for output in dests:
                    pulses[to_send] += 1
                    # print(label, '-low->' if to_send == 0 else '-high->', output)
                    stack.append((output, to_send, label))

                if label in {'sb', 'nd', 'ds', 'hf'}:
                    # if sum(modules[label]['inputs'].values()) > 1 :
                    #     print(i, modules[label]['inputs'])
                    if sum(modules[label]['inputs'].values()) == 0:
                        print(i, modules[label]['inputs'])
                        # input()

    print(pulses)
    return math.prod(pulses.values())

# too low: 1119935629956

# 151202 {'zq': 0}
# 151879 {'vv': 0}
# 152762 {'nt': 0}
# 153052 {'vn': 0}
#
# 155079 {'zq': 0}
# 155676 {'vv': 0}
# 156679 {'nt': 0}
# 156785 {'vn': 0}
#
# diffs:
# 3877
# 3797
# 3917
# 3733
#
# LCM = 215252378794009
# oh that worked

setday(20)

data = parselines()
# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
