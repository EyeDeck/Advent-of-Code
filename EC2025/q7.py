from ec import *


def p1():
    names, rules_raw = parse_double_break(1)
    names = names.split(',')
    rules_raw = rules_raw.split('\n')
    rules = {}
    for rule in rules_raw:
        print(rule)
        l,r = rule.split(' > ')
        rules[l] = set()
        for c in r.split(','):
            rules[l].add(c)

    print(rules)

    for name in names:
        for i in range(len(name)-1):
            l,r = name[i], name[i+1]
            print(l,r)
            if l not in rules:
                break
            if r not in rules[l]:
                break
        else:
            return name
    return


def p2():
    names, rules_raw = parse_double_break(2)
    names = names.split(',')
    rules_raw = rules_raw.split('\n')
    rules = {}
    for rule in rules_raw:
        print(rule)
        l,r = rule.split(' > ')
        rules[l] = set()
        for c in r.split(','):
            rules[l].add(c)

    print(rules)

    acc = 0
    for index, name in enumerate(names):
        for i in range(len(name)-1):
            l,r = name[i], name[i+1]
            print(l,r)
            if l not in rules:
                break
            if r not in rules[l]:
                break
        else:
            acc += index + 1

    return acc


def p3():
    names, rules_raw = parse_double_break(3)
    names = names.split(',')
    rules_raw = rules_raw.split('\n')
    rules = {}
    for rule in rules_raw:
        print(rule)
        l,r = rule.split(' > ')
        rules[l] = set()
        for c in r.split(','):
            rules[l].add(c)

    print(rules)

    valid_prefixes = []
    for index, name in enumerate(names):
        for i in range(len(name)-1):
            l,r = name[i], name[i+1]
            print(l,r)
            if l not in rules:
                break
            if r not in rules[l]:
                break
        else:
            valid_prefixes.append(name)

    seen = set()
    for prefix in valid_prefixes:
        q = [prefix]

        parent = {}

        print(q)
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
                parent[n] = cur
                q.append(n)

    return sum(1 for name in seen if 7 <= len(name) <= 11)



setquest(7)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
