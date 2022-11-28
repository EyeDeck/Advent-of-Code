import sys
import re


def pop_pairs(s):
    while True:
        s2 = re.sub('\[]|\(\)|<>|{}', '', s)
        if s2 == s:
            return s2
        s = s2


def solve():
    p1_score = 0
    p2_scores = []
    for line in data:
        pared = pop_pairs(line)
        for i in range(len(pared) - 1):
            l,r = pared[i:i+2]
            if l in brackets and r not in brackets and brackets[l] != r:
                p1_score += scores_p1[r]
                break
        else:
            to_add = [brackets[c] for c in reversed(pared)]
            sc = 0
            for c in to_add:
                sc = sc * 5 + scores_p2[c]
            p2_scores.append(sc)
    return p1_score, p2_scores[len(p2_scores) // 2]


day = 10
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

brackets = {'[': ']', '<': '>', '{': '}', '(': ')'}
scores_p1 = {')': 3, ']': 57, '}': 1197, '>': 25137}
scores_p2 = {')': 1, ']': 2, '}': 3, '>': 4}

solutions = solve()
print(f'part1: {solutions[0]}')
print(f'part2: {solutions[1]}')
