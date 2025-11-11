from ec import *


def construct_sword(sword):
    spine = [[None, sword[0], None]]
    for i in sword[1:]:
        for segment in spine:
            if i < segment[1] and segment[0] is None:
                segment[0] = i
                break
            elif i > segment[1] and segment[2] is None:
                segment[2] = i
                break
        else:
            spine.append([None, i, None])
    return spine


def get_quality(sword):
    return int(''.join([str(l[1]) for l in sword]))


def p1():
    sword = construct_sword(parse_lines(1, get_ints)[0][1:])
    return get_quality(sword)


def p2():
    data = parse_lines(2, get_ints)
    swords = {}
    for line in data:
        sword = construct_sword(line[1:])
        swords[line[0]] = get_quality(sword)

    return max(swords.values()) - min(swords.values())


def p3():
    data = parse_lines(3, get_ints)
    swords = {}
    for line in data:
        identifier = line[0]
        sword = construct_sword(line[1:])
        quality = get_quality(sword)
        sort_priority = [quality]
        for segment in sword:
            sort_priority.append(int(''.join(str(n) for n in segment if n is not None)))
        sort_priority.append(identifier)
        swords[identifier] = sort_priority

    sorted_swords = sorted(swords.items(), key=itemgetter(1), reverse=True)
    return sum(((i + 1) * n) for i, n in enumerate(s[0] for s in sorted_swords))


setquest(5)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
