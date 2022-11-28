import sys


def solve():
    state = {}
    for k, v in stats.items():
        state[k] = {'dist': 0, 'moving': True, 'time': v['stam'], 'points': 0}
    for i in range(1, 2503 + 1):
        for k, v in state.items():
            if v['moving']:
                v['dist'] += stats[k]['speed']
                v['time'] -= 1
                if v['time'] == 0:
                    v['moving'] = False
                    v['time'] = stats[k]['cd']
            else:
                v['time'] -= 1
                if v['time'] == 0:
                    v['moving'] = True
                    v['time'] = stats[k]['stam']
        leads = sorted(state, key=lambda k: state[k]['dist'])
        for k in leads:
            if state[k]['dist'] == state[leads[-1]]['dist']:
                state[k]['points'] += 1
        # print(i, ':')
        # for k, v in state.items():
        #     print(k, v)

    return max([state[k]['dist'] for k in state.keys()]), max([state[k]['points'] for k in state.keys()])


day = 14
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

stats = {}
with open(f) as file:
    for line in file:
        sp = line.split()
        stats[sp[0]] = {'speed': int(sp[3]), 'stam': int(sp[6]), 'cd': int(sp[-2])}

print('part1: %s\npart2: %s' % solve())
