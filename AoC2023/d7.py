import collections
from aoc import *


def get_type(cards, p2=False):
    counted = collections.Counter(cards)
    cts = [counted[k] for k in counted.keys()]
    cts.sort(reverse=True)

    if p2 and 'J' in counted and cts[0] != 5:
        cts.remove(counted['J'])
        cts[0] += counted['J']

    if cts[0] == 5:
        return 0  # Five of a kind
    elif cts[0] == 4:
        return 1  # Four of a kind
    elif cts[0] == 3:
        if cts[1] == 2:
            return 2  # Full house
        else:
            return 3  # Three of a kind
    elif cts[0] == 2:
        if cts[1] == 2:
            return 4  # Two pair
        else:
            return 5  # One pair
    else:
        return 6


def solve(p2):
    order = 'AKQT98765432J' if p2 else 'AKQJT98765432'
    repl = {c: string.ascii_lowercase[i] for i, c in enumerate(order)}
    hands = []
    for line in data:
        cards, bid = line.split()
        processed = str(get_type(cards, p2)) + ''.join(repl[k] for k in cards)
        hands.append((processed, cards, int(bid)))
    hands.sort(reverse=True)
    acc = 0
    for i, (processed, cards, bid) in enumerate(hands):
        acc += (i + 1) * bid
    return acc


setday(7)

data = parselines()

print('part1:', solve(False) )
print('part2:', solve(True) )
