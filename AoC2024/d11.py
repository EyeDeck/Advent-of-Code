from aoc import *


def solve(n):
    def tick(bins):
        new_bins = defaultdict(int)

        for stone, ct in bins.items():
            s = str(stone)
            if stone == 0:
                new_bins[1] += ct
            elif len(s) % 2 == 0:
                new_bins[int(s[:len(s) // 2])] += ct
                new_bins[int(s[len(s) // 2:])] += ct
            else:
                new_bins[stone * 2024] += ct

        return new_bins

    bins = defaultdict(int)

    for k in data:
        bins[k] += 1

    for i in range(n):
        bins = tick(bins)

    return sum(bins.values())


setday(11)

with open_default() as file:
    data = get_ints(file.read())

print('part1:', solve(25))
print('part2:', solve(75))
