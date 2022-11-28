import sys


def solve():
    tgt = 150
    ln = len(data)
    active = [frozenset([i]) for i in range(ln)]
    ct = 0
    best = 1000
    best_ct = 0
    seen = set()
    while active:
        cur = active.pop()
        for i in range(ln):
            if i in cur:
                continue
            nxt = frozenset(sorted([j for j in cur] + [i]))
            s = sum(data[i] for i in nxt)
            # print(nxt, [data[i] for i in nxt], s, ' <-------' if s == tgt else '')

            if nxt in seen:
                continue
            seen.add(nxt)

            if s < tgt:
                active.append(nxt)
            elif s == tgt:
                if len(nxt) == best:
                    best_ct += 1
                elif len(nxt) < best:
                    best = len(nxt)
                    best_ct = 1
                ct += 1
    return ct, best_ct


def p2():
    return None


day = 17
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    # data = sorted([int(i) for i in file.read().split()])
    data = [int(i) for i in file.read().split()]

print('part1: %s\npart2: %s' % solve())
