import math
from aoc import *


def solve():
    modules = {}
    for line in data:
        line = line.split('->')
        kind = line[0][0]
        label = line[0][1 if kind != 'b' else 0:].strip()
        dests = tuple(c.strip() for c in line[1].strip().split(','))

        modules[label] = {'state':0, 'type':kind, 'dests':dests}
        modules[label]['inputs'] = {}

    for (name, module) in list(modules.items()):
        for output in module['dests']:
            if output not in modules:  # because rx...
                modules[output] = {'state': 0, 'type': '?', 'dests': tuple(), 'inputs': {}}
            out_module = modules[output]
            out_module['inputs'][name] = 0

    seen = {}
    if 'rx' in modules:
        rx = modules['rx']
        rx_in = modules[next(iter(rx['inputs']))]['inputs'].keys()
        seen = {k:(-1, -1, -1) for k in rx_in}

    pulses = {0:0, 1:0}
    p1 = '?'

    for i in range(1,1000000):
        stack = deque([('broadcaster', 0, 'button')])
        pulses[0] += 1
        while stack:
            label, pulse, sender = stack.popleft()
            module = modules[label]
            dests = module['dests']
            kind = module['type']

            if kind == 'b':
                for output in dests:
                    stack.append((output, 0, label))
                    pulses[0] += 1
                    # if verbose:
                    #     print(label, '-low->', output)

            elif kind == '%':  # Flip-flop
                if pulse == 1:
                    continue
                module['state'] = module['state'] ^ 1
                to_send = 1 if module['state'] else 0
                for output in dests:
                    pulses[to_send] += 1
                    stack.append((output, to_send, label))
                    # if verbose:
                    #     print(label, '-low->' if to_send == 0 else '-high->', output)

            elif kind == '&':  # Conjunction
                module['inputs'][sender] = pulse
                to_send = 0 if sum(module['inputs'].values()) == len(module['inputs']) else 1
                for output in dests:
                    pulses[to_send] += 1
                    stack.append((output, to_send, label))
                    # if verbose:
                    #     print(label, '-low->' if to_send == 0 else '-high->', output)

                # really awkward cycle detection code for part 2
                if label in seen and sum(modules[label]['inputs'].values()) == 0:
                    last = seen[label]
                    if last[2] < 1:
                        seen[label] = (i, last[1], last[2]+1)
                    elif last[2] == 1:
                        seen[label] = (i - last[0], -1, 2)

                    if verbose:
                        print(i, label, seen)

                    if all(d[2] == 2 for d in seen.values()):
                        return p1, math.lcm(*[d[0] for d in seen.values()])

        if i == 1000:
            p1 = math.prod(pulses.values())

    return p1, '?'

setday(20)

data = parselines()

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1: %s\npart2: %s' % solve())
