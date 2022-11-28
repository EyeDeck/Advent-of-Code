import sys
from collections import *


def p1(pl1, pl2):
    pl1 = deque([int(i) for i in pl1.split('\n')[1:]])
    pl2 = deque([int(i) for i in pl2.split('\n')[1:]])

    while len(pl1) and len(pl2):
        c1, c2 = pl1.popleft(), pl2.popleft()
        # print('Player 1 plays', c1, '\n', 'Player 2 plays', c2)
        if c1 > c2:
            pl1.append(c1)
            pl1.append(c2)
        else:
            pl2.append(c2)
            pl2.append(c1)
        # print("Player 1's deck:", pl1)
        # print("Player 2's deck:", pl2)

    if len(pl1):
        winner = pl1
    else:
        winner = pl2

    s = 0
    for i,c in enumerate(reversed(winner)):
        s += (i+1) * c

    print(' winner was:', 1 if pl1==winner else 2)
    return s


def rcombat(depth, pl1, pl2, scores):
    # print("RECURSED", depth, pl1, pl2)
    seen = set()
    rnd = 0
    while len(pl1) and len(pl2):
        handset = (tuple(pl1), tuple(pl2))
        if handset in seen:
            return 1, pl1
        else:
            seen.add(handset)
            # print("Player 1's deck:", pl1)
            # print("Player 2's deck:", pl2)
            rnd += 1
            c1, c2 = pl1.popleft(), pl2.popleft()
            if c1 <= len(pl1) and c2 <= len(pl2):
                winner, deck = rcombat(depth+1, deque(pl1[i] for i in range(c1)),  deque(pl2[i] for i in range(c2)), scores)
            #    print('UNRECURSED to ', depth)
            else:
                winner = 1 if c1 > c2 else 2
            # print('winner:', winner)

            if winner == 1:
                pl1.append(c1)
                pl1.append(c2)
            else:
                pl2.append(c2)
                pl2.append(c1)
    # print(pl1 if winner == 1 else pl2)
    return winner, pl1 if winner == 1 else pl2


def p2(pl1, pl2):
    scores = [0,0]
    pl1 = deque([int(i) for i in pl1.split('\n')[1:]])
    pl2 = deque([int(i) for i in pl2.split('\n')[1:]])

    winner, deck = rcombat(1, pl1, pl2, scores)

    s = 0
    for i, c in enumerate(reversed(deck)):
        s += (i + 1) * c

    print(' winner was:', winner)
    return s


f = 'd22.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    player1, player2 = file.read().strip().split('\n\n')

print(f'part1: {p1(player1, player2)}')
print(f'part2: {p2(player1, player2)}')
