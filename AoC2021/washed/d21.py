import sys
from collections import defaultdict
from functools import lru_cache

die = 0


def roll100():
    global die
    die = die % 100 + 1
    return die


def p1(pl1, pl2):
    sc1 = 0
    sc2 = 0
    i = 0
    while True:
        moves1 = roll100() + roll100() + roll100()
        i += 3
        pl1 = (pl1 - 1 + moves1) % 10 + 1
        sc1 += pl1
        if sc1 >= 1000:
            return sc2 * i

        moves2 = roll100() + roll100() + roll100()
        i += 3
        pl2 = (pl2 - 1 + moves2) % 10 + 1
        sc2 += pl2
        # print(f'{i} pl1={pl1}, moves={moves1}, score={sc1},   pl2={pl2}, moves={moves2}, score={sc2}')
        if sc2 >= 1000:
            return sc1 * i


def nxt(p, steps):
    return ((p + steps - 1) % 10) + 1


@lru_cache(maxsize=None)
def p2(turn, pl1, pl2, sc1, sc2):
    if sc1 >= 21:
        return 1, 0
    elif sc2 >= 21:
        return 0, 1

    r1, r2 = 0, 0
    for k, v in outcomes.items():
        if turn == 0:
            result = p2(1, nxt(pl1, k), pl2, sc1 + nxt(pl1, k), sc2)
            r1 += v * result[0]
            r2 += v * result[1]
        else:
            result = p2(0, pl1, nxt(pl2, k), sc1, sc2 + nxt(pl2, k))
            r1 += v * result[0]
            r2 += v * result[1]
    return r1, r2


day = 21

if len(sys.argv) >= 2:
    in_pl1, in_pl2 = [int(i) for i in sys.argv[1:]]
else:
    f = sys.argv[1] if len(sys.argv) > 1 else f'd{day}.txt'
    with open(f) as file:
        data = [[word for word in line.split()] for line in file.read().strip().split('\n')]
        in_pl1, in_pl2 = int(data[0][-1]), int(data[1][-1])

outcomes = defaultdict(int)
for d1 in range(1, 4):
    for d2 in range(1, 4):
        for d3 in range(1, 4):
            outcomes[d1 + d2 + d3] += 1

print(f'part1: {p1(in_pl1, in_pl2)}')
# print(f'part2: {max(p2(0, in_pl1, in_pl2, 0, 0))}')
print(f'part2: {p2(0, in_pl1, in_pl2, 0, 0)}')
