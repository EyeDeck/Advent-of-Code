from aoc import *

def solve():
    acc = 0
    cards = {}
    copies = {}

    for line in data:
        card, r = line.split(':')
        card = int(card.split()[-1])
        l,r = r.split('|')
        targets = {int(n) for n in l.strip().split()}
        matches = {int(n) for n in r.strip().split()}

        cards[card] = [targets, matches]
        copies[card] = 1

    for card_id, (targets, matches) in cards.items():
        match_ct = len(targets & matches)
        acc += (2 ** match_ct) >> 1
        for i in range(card_id + 1, card_id + match_ct + 1):
            copies[i] += copies[card_id]

    return acc, sum(copies.values())


setday(4)

data = parselines()

print('part1: %s\npart2: %s' % solve())
