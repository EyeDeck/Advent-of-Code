import collections
from aoc import *


def p1():
    def get_type(cards):
        counted = collections.Counter(cards)
        # print(counted)
        cts = [counted[k] for k in counted.keys()]
        cts.sort()
        cts.reverse()
        # print(cts)
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

    repl = {c:string.ascii_lowercase[i] for i,c in enumerate('AKQJT98765432')}
    # print(repl)
    hands = []
    for line in data:
        cards, bid = line.split()
        type = get_type(cards)
        processed = str(type) + ''.join(repl[k] for k in cards)
        hands.append((processed, int(bid)))
    hands.sort()
    hands.reverse()
    acc = 0
    for i, (cards, bid) in enumerate(hands):
        # print(i, cards, bid)
        acc += (i+1) * bid
    return acc

# not 251236888


def p2():
    def get_type(cards):
        counted = collections.Counter(cards)
        print(counted)
        cts = [counted[k] for k in counted.keys()]
        cts.sort()
        cts.reverse()
        print(cts)
        if 'J' in counted and cts[0] != 5:
            cts.remove(counted['J'])
            cts[0] += counted['J']
            print('\r added', counted['J'], cts)

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

    repl = {c: string.ascii_lowercase[i] for i, c in enumerate('AKQT98765432J')}
    # print(repl)
    hands = []
    for line in data:
        cards, bid = line.split()
        type = get_type(cards)
        processed = str(type) + ''.join(repl[k] for k in cards)
        hands.append((processed, cards, int(bid)))
    hands.sort()
    hands.reverse()
    acc = 0
    for i, (processed, cards, bid) in enumerate(hands):
        print(i, processed, cards, bid)
        acc += (i + 1) * bid
    return acc


setday(7)

data = parselines()

print('part1:', p1() )
print('part2:', p2() )
