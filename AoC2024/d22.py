from aoc import *


def tick(n):
    n = ((n * 64) ^ n) % 16777216
    n = ((n // 32) ^ n) % 16777216
    n = ((n * 2048) ^ n) % 16777216
    return n


def p1():
    acc = 0
    for line in data:
        secret = line[0]
        for _ in range(2000):
            secret = tick(secret)
        acc += secret

    print(tick(123))

    return acc


def p2():
    monkey_changes = []
    for line in data:
        secret = line[0]
        nums = [secret % 10]
        for _ in range(2000):
            secret = tick(secret)
            nums.append(secret % 10)
            # print(secret, nums)
            # input()
        monkey_changes.append(nums)

    seen = set()
    diff_data = []
    for monkey_data in monkey_changes:
        diff_datum = {}
        for i in range(len(monkey_data) - 4):
            ns = monkey_data[i:i + 5]
            # print(ns)
            diff_seq = tuple(ns[i + 1] - ns[i] for i in range(len(ns) - 1))
            seen.add(diff_seq)
            if diff_seq not in diff_datum:
                diff_datum[diff_seq] = ns[-1]
            # print(diff_seq, '=', ns[-1])
        # input()
        diff_data.append(diff_datum)

    best = 0
    best_set = None
    for diff_set in seen:
        acc = 0
        for diff_datum in diff_data:
            if diff_set in diff_datum:
                acc += diff_datum[diff_set]
        # best = max(acc, best)
        if acc > best:
            best = acc
            best_set = diff_set
    print(best_set)
    return best


setday(22)

data = parselines(get_ints)

print('part1:', p1())
print('part2:', p2())