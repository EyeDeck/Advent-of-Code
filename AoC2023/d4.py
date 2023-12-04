from aoc import *

def p1():
    acc = 0
    for line in data:
        card, r = line.split(':')
        card = int(card.split()[-1])
        l,r = r.split('|')
        targets = [int(n) for n in l.strip().split()]
        matches = {int(n) for n in r.strip().split()}

        v = 0
        for tgt in targets:
            if tgt in matches:
                if v == 0:
                    v = 1
                else:
                    v *= 2
        acc += v
    return acc


def p2():
    cards = {}
    copies = {}

    for line in data:
        card, r = line.split(':')
        card = int(card.split()[-1])
        l,r = r.split('|')
        targets = [int(n) for n in l.strip().split()]
        matches = {int(n) for n in r.strip().split()}

        cards[card] = [targets, matches]
        copies[card] = 1

    for card_id, (targets, matches) in cards.items():
        match_ct = 0
        for tgt in targets:
            if tgt in matches:
                match_ct += 1

        for i in range(card_id + 1, card_id + match_ct + 1):
            copies[i] += copies[card_id]

    return sum(copies.values())


setday(4)

data = parselines()

print('part1:', p1() )
print('part2:', p2() )
