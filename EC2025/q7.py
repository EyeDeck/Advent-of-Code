from ec import *


def parse_n(n):
    names, rules_raw = parse_double_break(n)
    names = names.split(',')
    rules_raw = rules_raw.split('\n')

    rules = {}
    for rule in rules_raw:
        l,r = rule.split(' > ')
        rules[l] = set()
        for c in r.split(','):
            rules[l].add(c)

    return names, rules


def validate_name(name, rules):
    for i in range(len(name) - 1):
        l, r = name[i], name[i + 1]
        if l not in rules:
            break
        if r not in rules[l]:
            break
    else:
        return True
    return False


def p1():
    names, rules = parse_n(1)

    for name in names:
        if validate_name(name, rules):
            return name


def p2():
    names, rules = parse_n(2)

    acc = 0
    for index, name in enumerate(names):
        if validate_name(name, rules):
            acc += index + 1

    return acc


def p3():
    names, rules = parse_n(3)

    valid_prefixes = []
    for index, name in enumerate(names):
        if validate_name(name, rules):
            valid_prefixes.append(name)

    acc = 0
    seen = set()
    for prefix in valid_prefixes:
        q = [prefix]

        parent = {}

        while q:
            cur = q.pop()
            if len(cur) > 11:
                continue

            for n in rules[cur[-1]]:
                n = cur + n
                if n in seen:
                    continue
                else:
                    seen.add(n)
                    if 7 <= len(n) <= 11:
                        acc += 1
                parent[n] = cur
                q.append(n)

    return acc


setquest(7)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
