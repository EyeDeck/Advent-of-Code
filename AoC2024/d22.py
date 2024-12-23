import collections

from aoc import *


def tick(n):
    n = ((n * 64) ^ n) % 16777216
    n = ((n // 32) ^ n) % 16777216
    n = ((n * 2048) ^ n) % 16777216
    return n


def solve():
    monkey_changes = []
    acc = 0
    for line_n, secret in enumerate(data):
        nums = [secret % 10]
        for _ in range(2000):
            secret = tick(secret)
            nums.append(secret % 10)
        acc += secret
        if line_n % 20 == 0:
            print(f'\r[{(line_n/len(data)*100):.2f}%] part1: {acc}', end='', flush=True)
        monkey_changes.append(nums)
    yield acc

    diff_data = collections.Counter()
    for line_n, monkey_data in enumerate(monkey_changes):
        diff_datum = collections.Counter()
        for i in range(len(monkey_data) - 4):
            diff_seq = tuple(monkey_data[i + j + 1] - monkey_data[i + j] for j in range(4))
            if diff_seq not in diff_datum:
                diff_datum[diff_seq] = monkey_data[i + 4]
        diff_data += diff_datum
        if line_n % 8 == 0:
            best = max(diff_data, key=diff_data.get)
            print(f'\r[{line_n/len(monkey_changes)*100:.2f}%] part2: {diff_data[best]} {tuple(best)}', end='', flush=True)
    yield max(diff_data.values())


setday(22)

data = [line[0] for line in parselines(get_ints)]

gen = solve()
print('\r\033[Kpart1:', next(gen), flush=True)
print('\r\033[Kpart2:', next(gen), flush=True)
