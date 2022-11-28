import re
import sys


def bag_contains(bag_contents, tgt):
    if tgt in bag_contents:
        return True
    else:
        for bag in bag_contents.keys():
            if bag_contains(data[bag], tgt):
                return True
    return False


def count_bags_in(bag_type):
    ct = 0
    for child_bag, holds in data[bag_type].items():
        ct += holds
        ct += count_bags_in(child_bag) * holds
    return ct


def p1():
    ct = 0
    for k, v in data.items():
        if bag_contains(v, 'shiny gold'):
            ct += 1
    return ct


def p2():
    return count_bags_in('shiny gold')


f = 'd7.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip().split('bags contain') for line in file]
data = {line[0].strip(): line[1] for line in data}

for k, v in data.items():
    d = {}
    bags = re.findall('([0-9] [a-z]+ [a-z]+) [a-z]+', v)
    for bag in bags:
        d[bag[2:]] = int(bag[0])
    data[k] = d

print(f'p1: {p1()}')
print(f'p2: {p2()}')
