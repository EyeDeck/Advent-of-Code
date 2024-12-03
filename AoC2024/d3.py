from aoc import *


def solve():
    acc = 0
    results = re.findall(r"(mul\((\d+),(\d+)\))", data)
    for r in results:
        acc += int(r[1]) * int(r[2])
    return acc


setday(3)

with open_default() as file:
    data = file.read().replace('\n', '')

print('part1:', solve())

data = re.sub(r"don't\(\).*?do\(\)", "do()", data)
print('part2:', solve())
