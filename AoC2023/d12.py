from aoc import *

# def p1():
#     parsed = []
#     acc = 0
#     for line in data:
#         cond, groups = line.split(' ')
#         # cond = [('.','#') if c == '?' else c for c in cond]
#         cond = [c for c in cond]
#         cond = [c for i, c in enumerate(cond) if c != '.' or i == 0 or not (c == '.' and cond[i-1] == '.')]
#         while cond[0] == '.':
#             cond.pop(0)
#         while cond[-1] == '.':
#             cond.pop()
#
#         groups = [int(i) for i in groups.split(',')]
#
#         possibilities = []
#         print(cond, groups)
#         for i, group in enumerate(groups):
#             before = groups[0:max(i,0)]
#             before = sum(before) + len(before)
#             after = groups[min(i+1, len(groups)):]
#             after = sum(after) + len(after)
#             box = cond[before:len(cond) - after]
#             print(group, ';', before, after, box)
#
#             if '#' * group in ''.join(cond):
#                 possibilities.append(1)
#                 continue
#
#         print('')
#
#     return acc


@memo
def dp(cond, groups):
    # print(cond, groups)

    if len(cond) == 0:
        return 1 if len(groups) == 0 else 0
    first = cond[0]
    if first == '.':
        return dp(cond[1:], groups)
    elif first == '#':
        if len(groups) == 0:
            return 0
        if len(cond) < groups[0]:
            return 0
        if any(c == '.' for c in cond[0:groups[0]]):
            return 0
        if len(groups) > 1:
            if len(cond) < groups[0] + 1 or cond[groups[0]] == '#':
                return 0
            return dp(cond[groups[0] + 1:], groups[1:])
        return dp(cond[groups[0]:], groups[1:])
    elif first == '?':
        return dp(('.',) + cond[1:], groups) + dp(('#',) + cond[1:], groups)
    return 0


def p1():
    acc = 0
    for line in data:
        cond, groups = line.split(' ')
        cond = tuple(c for c in cond)

        groups = tuple(int(i) for i in groups.split(','))

        possibilities = dp(cond, groups)
        # print(possibilities, '\n')
        acc += possibilities
    return acc


def p2():
    acc = 0
    for line in data:
        cond, groups = line.split(' ')

        cond = '?'.join((cond for _ in range(5)))
        cond = tuple(c for c in cond)

        groups = ','.join((groups for _ in range(5)))
        groups = tuple(int(i) for i in groups.split(','))

        possibilities = dp(cond, groups)
        # print(possibilities, '\n')
        acc += possibilities
    return acc


setday(12)

data = parselines()

print('part1:', p1() )
print('part2:', p2() )
