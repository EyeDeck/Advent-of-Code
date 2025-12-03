from aoc import *


def solve(n):
    s_range = [str(i) for i in range(9,0,-1)]
    acc = 0
    for line in data:
        found = []
        current_index = 0
        for limit in range(n, 0, -1):
            l, r = current_index, len(line) - limit + 1
            for s in s_range:
                pos = line.find(s, l, r)
                if pos >= 0:
                    s = line[pos]
                    found.append(s)
                    current_index = pos + 1
                    break
        best = int(''.join(found))
        acc += best
    return acc


if __name__ == '__main__':
    setday(3)

    data = parselines()

    print('part1:', solve(2))
    print('part2:', solve(12))
