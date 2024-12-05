from aoc import *


def verify(pageset, rules_before):
    for i, page in enumerate(pageset):
        pages_after = pageset[i + 1:]
        for j, page_after in enumerate(pages_after):
            if page_after in rules_before[page]:
                pageset[i+j+1], pageset[i] = pageset[i], pageset[i+j+1]
                return False
    return pageset[len(pageset) // 2]


def solve():
    # set must go BEFORE key
    rules_before = defaultdict(set)

    for rule in rules_raw:
        rules_before[rule[1]].add(rule[0])

    acc_p1 = 0
    acc_p2 = 0
    for pageset in pagesets_raw:
        r = verify(pageset, rules_before)
        if r:
            acc_p1 += r
            continue
        while True:
            r = verify(pageset, rules_before)
            if r:
                acc_p2 += r
                break

    return acc_p1, acc_p2


setday(5)

with open_default() as file:
    rules_raw, pagesets_raw = file.read().split('\n\n')

rules_raw = [[int(i) for i in line.split('|')] for line in rules_raw.split('\n')]
pagesets_raw = [[int(i) for i in line.split(',')] for line in pagesets_raw.split('\n')]


print('part1: %d\npart2: %d' % solve())
