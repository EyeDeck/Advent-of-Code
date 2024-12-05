from aoc import *


def verify(pageset, rules_before, rules_after, fix=False):
    print(pageset)
    for i, page in enumerate(pageset):
        pages_before = pageset[:i]
        pages_after = pageset[i + 1:]
        for j, page_before in enumerate(pages_before):
            if page_before in rules_after[page]:
                print('a', i,i+j+1)
                if fix:
                    pageset[i+j+1], pageset[i] = pageset[i], pageset[i+j+1]
                return False
        for j, page_after in enumerate(pages_after):
            if page_after in rules_before[page]:
                print('b', i,i+j+1)
                if fix:
                    pageset[i+j+1], pageset[i] = pageset[i], pageset[i+j+1]
                return False
        print(page, pages_before, pages_after)
    return pageset[len(pageset) // 2]


def p1():
    # set must go BEFORE key
    rules_before = defaultdict(set)
    # set must go AFTER key
    rules_after = defaultdict(set)

    for rule in rules_raw:
        rules_before[rule[1]].add(rule[0])
        rules_after[rule[0]].add(rule[1])
    print(rules_before)
    print(rules_after)

    acc = sum(verify(pageset, rules_before, rules_after) for pageset in pagesets_raw)
    return acc


def p2():
    # set must go BEFORE key
    rules_before = defaultdict(set)
    # set must go AFTER key
    rules_after = defaultdict(set)

    for rule in rules_raw:
        rules_before[rule[1]].add(rule[0])
        rules_after[rule[0]].add(rule[1])
    print(rules_before)
    print(rules_after)

    bad_pagesets = []
    for pageset in pagesets_raw:
        if not verify(pageset, rules_before, rules_after, True):
            bad_pagesets.append(pageset)
    print(bad_pagesets)

    fixed_pagesets = []
    for pageset in bad_pagesets:
        while not verify(pageset, rules_before, rules_after, True):
            pass
        fixed_pagesets.append(pageset)
        print('fixed:', pageset)

    acc = sum(verify(pageset, rules_before, rules_after) for pageset in fixed_pagesets)
    return acc


setday(5)

with open_default() as file:
    rules_raw, pagesets_raw = file.read().split('\n\n')

rules_raw = [[int(i) for i in line.split('|')] for line in rules_raw.split('\n')]
pagesets_raw = [[int(i) for i in line.split(',')] for line in pagesets_raw.split('\n')]


print('part1:', p1() )
print('part2:', p2() )
