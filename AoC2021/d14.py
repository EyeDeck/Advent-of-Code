import sys
from collections import *


def step(polymer):
    new_polymer = defaultdict(int)
    for k, v in polymer.items():
        new_polymer[k[0] + rules[k]] += v
        new_polymer[rules[k] + k[1]] += v
    return new_polymer


def solve_for(n):
    polymer = defaultdict(int)
    for i in range(len(template) - 1):
        polymer[''.join((template[i], template[i + 1]))] += 1
    for i in range(n):
        polymer = step(polymer)
    elements = defaultdict(int)
    for k, v in polymer.items():
        elements[k[0]] += v
    elements[template[-1]] += 1  # correct for not counting the very last element
    return max(elements.values()) - min(elements.values())


day = 14
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    template, rules = file.read().split('\n\n')

rules = {(x := line.strip().split(' -> '))[0]: x[1] for line in rules.split('\n')}

print(f'part1: {solve_for(10)}')
print(f'part2: {solve_for(40)}')

if len(sys.argv) >= 3:
    print(f'part3: {solve_for(int(sys.argv[2]))}')
