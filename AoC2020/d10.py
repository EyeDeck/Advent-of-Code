import sys
from collections import defaultdict


# this was the wrong solution and I'm a retard
# (works on the small inputs tho)
# def p1():
#     adapter = max(data) + 3
#     data_set = set(data)
#     queue = [[adapter]]
#     found = []
#     while queue:
#         cur = queue.pop(0)
#
#         if len(cur)-1 == len(data_set):
#             found = cur
#             break
#         print(len(cur))
#
#         leading = cur[-1]
#         adjacent = set()
#         for i in range(leading-3, leading):
#             if i in data_set:
#                 adjacent.add(i)
#         for i in adjacent:
#             to_append = cur + [i]
#             queue.append(to_append)
#         # print(adjacent)
#         # print(queue)
#     one_dif = 0
#     three_dif = 0
#     for i, n in enumerate(found[:-1]):
#         next = found[i+1]
#         if next == n-3:
#             # print(n, next, 'three')
#             three_dif += 1
#         elif next == n-1:
#             one_dif += 1
#     # print(one_dif, three_dif)
#
#     return one_dif * three_dif


def p1():
    one_dif = 0
    three_dif = 0
    for i, n in enumerate(data[:-1]):
        n2 = data[i + 1]
        if n2 == n+1:
            one_dif += 1
        elif n2 == n+3:
            three_dif += 1
    return one_dif * three_dif


def p2():
    dp = defaultdict(int)
    dp[0] = 1
    for n in data:
        dp[n] += dp[n-1] + dp[n-2] + dp[n-3]
    return dp[max(dp)]


f = 'd10.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = sorted([int(line.strip()) for line in file.readlines()])
    data.append(max(data) + 3)
    data.insert(0, 0)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
