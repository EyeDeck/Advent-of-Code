from aoc import *

def firstnum(line, reverse, replace):
    i = len(line)-1 if reverse else 0
    while (reverse and i >= 0) or (i <= len(line)):
        if line[i].isdigit():
            return line[i]
        if replace:
            for n, v in enumerate(num_strs):
                if line[i:i + len(v)] == v:
                    return str(n)
        i = i - 1 if reverse else i + 1
    die()

def solve(replace):
    acc = 0
    for line in data:
        acc += int(firstnum(line, False, replace) + firstnum(line, True, replace))
    return acc


setday(1)

data = parselines()
num_strs = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

print('part1:', solve(False) )
print('part2:', solve(True) )
