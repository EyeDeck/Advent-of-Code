import sys
from collections import defaultdict
from functools import lru_cache

die = 0


def roll100():
    global die
    die = die % 100 + 1
    return die


def p1(pl1, pl2):
    sc1, sc2, rolls = 0, 0, 0

    while True:
        moves1 = roll100() + roll100() + roll100()
        rolls += 3
        pl1 = tile(pl1, moves1)
        sc1 += pl1
        if sc1 >= 1000:
            return sc2 * rolls

        moves2 = roll100() + roll100() + roll100()
        rolls += 3
        pl2 = tile(pl2, moves2)
        sc2 += pl2
        # print(f'{rolls} pl1={pl1}, moves={moves1}, score={sc1},   pl2={pl2}, moves={moves2}, score={sc2}')
        if sc2 >= 1000:
            return sc1 * rolls


def tile(place, adv):
    return (place - 1 + adv) % 10 + 1


# the memo speeds this up a bunch but is not strictly necessary
# @lru_cache(maxsize=None)
def p2(pl1, pl2, turn, sc1, sc2, tgt):
    if sc1 >= tgt:
        return 1, 0
    if sc2 >= tgt:
        return 0, 1

    score1, score2 = 0, 0
    # for d, mult in outcomes.items():
    #     if turn == 0:
    #         t = tile(pl1, d)
    #         scores = p2(t, pl2, 1, sc1 + t, sc2, tgt)
    #     else:
    #         t = tile(pl2, d)
    #         scores = p2(pl1, t, 0, sc1, sc2 + t, tgt)
    #     score1 += mult * scores[0]
    #     score2 += mult * scores[1]

    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                d = a+b+c
                if turn == 0:
                    t = tile(pl1, d)
                    scores = p2(t, pl2, 1, sc1 + t, sc2, tgt)
                else:
                    t = tile(pl2, d)
                    scores = p2(pl1, t, 0, sc1, sc2 + t, tgt)
                score1 += scores[0]
                score2 += scores[1]

    return score1, score2


day = 21

if len(sys.argv) >= 2:
    in_pl1, in_pl2 = [int(i) for i in sys.argv[1:]]
else:
    f = sys.argv[1] if len(sys.argv) > 1 else f'd{day}.txt'
    with open(f) as file:
        data = [[word for word in line.split()] for line in file.read().strip().split('\n')]
        in_pl1, in_pl2 = int(data[0][-1]), int(data[1][-1])

# we can precalc the number of distinct Dirac die outcomes for a set of 3 rolls, and save a ridiculous amount of
# unnecessary recursion by multiplying with these later, so much so this is solvable even without memoization
outcomes = defaultdict(int)
for a in range(1, 4):
    for b in range(1, 4):
        for c in range(1, 4):
            outcomes[a + b + c] += 1

print(f'part1: {p1(in_pl1, in_pl2)}')
print(f'part2: {max(p2(in_pl1, in_pl2, 0, 0, 0, 21))}')
