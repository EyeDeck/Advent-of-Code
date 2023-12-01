from aoc import *

def firstnum(line, reverse, replace):
    rpl = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "zero": 0}
    i = len(line)-1 if reverse else 0
    while (reverse and i >= 0) or (i <= len(line)):
        if line[i].isdigit():
            return line[i]
        if replace:
            for k, v in rpl.items():
                if line[i:i + len(k)] == k:
                    return str(v)
        i = i - 1 if reverse else i + 1
    die()

def solve(replace):
    acc = 0
    for line in data:
        acc += int(firstnum(line, False, replace) + firstnum(line, True, replace))
    return acc


setday(1)

data = parselines()

print('part1:', solve(False) )
print('part2:', solve(True) )
