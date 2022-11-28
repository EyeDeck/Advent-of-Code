import sys
from collections import defaultdict


def p1():
    return sum([len([j for j in i[1] if len(j) in (2, 3, 4, 7)]) for i in data])


def p2():
    cum = 0
    for line in data:
        left, right = line
        possibilities = {x: letters.copy() for x in letters}
        # this loop may be omitted, but it increases runtime by ~20-50x
        for digit in left:
            dlen = len(digit)
            if dlen in known_lens and len(known_lens[dlen]) == 1:
                n = known_lens[dlen][0]
                for dg in digit:
                    for char in letters:
                        # print(n, dlen, dg, char)
                        if char not in valid[n] and dg in possibilities[char]:
                            possibilities[char].remove(dg)
        chosen = {}
        trns = do_search(0, possibilities, chosen, line)
        cum += int(''.join([str(i) for i in [valid_r[''.join(sorted(d.translate(trns)))] for d in right]]))
    return cum


def do_search(n, ps, ch, line):
    if n == 7:
        return test_mapping(ch, line)
    this_letter = letters[n]
    for i, c in enumerate(ps[this_letter]):
        if c in ch:
            continue
        chosen = ch.copy()
        chosen[c] = this_letter
        result = do_search(n + 1, ps, chosen, line)
        if result:
            return result


def test_mapping(mapping, chars):
    trns = ''.maketrans(mapping)
    for side in chars:
        for char in side:
            if frozenset(char.translate(trns)) not in valid_r_set:
                return False
    return trns


day = 8
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[half.strip().split(' ') for half in line.strip().split('|')] for line in file]
    letters = [c for c in 'abcdefg']
    valid = {0:'abcefg', 1:'cf', 2:'acdeg', 3:'acdfg', 4:'bcdf', 5:'abdfg', 6:'abdefg', 7:'acf', 8:'abcdefg', 9:'abcdfg'}
    valid_r = {v: k for k, v in valid.items()}
    valid_r_set = {frozenset(v): k for k, v in valid.items()}
    known_lens = defaultdict(list)
    for k,v in valid.items():
        known_lens[len(v)].append(k)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
