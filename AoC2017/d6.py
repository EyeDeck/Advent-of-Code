import operator
from aoc import *


def solve():
    cur = data.copy()
    seen = set()
    cycle = 0
    first_dupe = None
    while True:
        hashable = tuple(cur)
        if first_dupe:
            if hashable == first_dupe:
                yield cycle
        elif hashable in seen:
            first_dupe = hashable
            yield cycle
            cycle = 0
        seen.add(hashable)
        max_index, max_value = max(enumerate(cur), key=operator.itemgetter(1))
        cur[max_index] = 0
        for i in range(max_value):
            cur[(max_index + i + 1) % len(cur)] += 1

        cycle += 1


setday(6)

data = parselines(get_ints)[0]

verbose = '-v' in sys.argv or '--verbose' in sys.argv

gen = solve()
print('part1:', next(gen))
print('part2:', next(gen))
