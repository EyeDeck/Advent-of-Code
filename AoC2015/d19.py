import heapq
import sys
from collections import *


def p1():
    seen = set()
    for repl, tgts in replacements.items():
        ln = len(repl)
        for i in range(len(molecule)):
            if molecule[i:i + ln] != repl:
                continue
            for tgt in tgts:
                seen.add(molecule[:i] + tgt + molecule[i + ln:])
    return len(seen)


# this works on the example...
# def get_adj(mol):
#     seen = set()
#     for repl, tgts in replacements_inv.items():
#         ln = len(repl)
#         for i in range(len(mol)-1,-1,-1):
#             if mol[i:i + ln] != repl:
#                 continue
#             for tgt in tgts:
#                 seen.add(mol[:i] + tgt + mol[i + ln:])
#     return seen
#
# def p2():
#     active = []
#     heapq.heappush(active, [len(molecule), 0, molecule])
#     i = 0
#     best_for = {}
#     while active:
#         cost, steps, cur = heapq.heappop(active)
#
#         if cur in best_for:
#             if steps < best_for[cur]:
#                 best_for[cur] = steps
#             else:
#                 continue
#         else:
#             best_for[cur] = steps
#
#         if i % 10000 == 0:
#             print(i, cost, steps, cur)
#         i += 1
#         # print(cost, steps, cur)
#         if cur == 'e':
#             return steps
#         for neighbor in get_adj(cur):
#             heapq.heappush(active, [len(neighbor), steps+1, neighbor])
#     return None


def find_first_replacement(mol):
    for i in range(len(mol) - 1, -1, -1):
        for repl in replacements_inv:
            ln = len(repl)
            if mol[i:i + ln] == repl:
                return mol[:i] + replacements_inv[repl] + mol[i + ln:]


# I'm pretty sure this only works on the input because of the way it's written
def p2():
    mol = molecule
    n = 0
    while mol != 'e':
        n += 1
        mol = find_first_replacement(mol)
    return n


day = 19
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    replacements_raw, molecule = file.read().split('\n\n')
replacements = defaultdict(set)
replacements_inv = {}
for line in replacements_raw.split('\n'):
    l, r = line.split(' => ')
    replacements[l].add(r)
    replacements_inv[r] = l
# print(replacements, molecule)
# print(replacements_inv)
# sys.exit()

print(f'part1: {p1()}')
print(f'part2: {p2()}')
