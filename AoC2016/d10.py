from aoc import *


def solve():
    mapping = defaultdict(dict)
    inv = defaultdict(list)
    stack = deque()
    for line in data:
        line = line.split()
        if line[0] == 'value':
            bot, has = int(line[-1]), int(line[1])
            inv[bot].append(has)
            if len(inv[bot]) == 2:
                stack.append(bot)
        elif line[0] == 'bot':
            bot, low, high = int(line[1]), int(line[6]), int(line[-1])
            if line[5] == 'output':
                low = (low * -1) - 1
            if line[10] == 'output':
                high = (high * -1) - 1
            mapping[bot][False] = low
            mapping[bot][True] = high

    p1 = None
    while stack:
        cur = stack.popleft()
        low, high = sorted(inv[cur])
        # print(stack, cur, low, high)

        if low == 17 and high == 61 and p1 is None:
            p1 = cur

        to_low, to_high = mapping[cur][False], mapping[cur][True]

        # turned out not to be necessary, but I think the right input could otherwise give 3 to one bot potentially
        if len(inv[to_low]) == 2 or len(inv[to_high]) == 2:
            stack.append(cur)
            continue

        inv[to_low].append(low)
        inv[to_high].append(high)
        del inv[cur]

        if len(inv[to_low]) == 2:
            stack.append(to_low)
        if len(inv[to_high]) == 2:
            stack.append(to_high)

    return p1, inv[-1][0] * inv[-2][0] * inv[-3][0]


setday(10)

data = parselines()

print('part1: %s\npart2: %s' % solve())
