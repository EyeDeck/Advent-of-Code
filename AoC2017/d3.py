from math import *

from aoc import *


# 37  36  35  34  33  32  31
# 38  17  16  15  14  13  30
# 39  18   5   4   3  12  29
# 40  19   6   1   2  11  28
# 41  20   7   8   9  10  27
# 42  21  22  23  24  25  26
# 43  44  45  46  47  48  49
# ring = ceil(sqrt(n)) // 2
# diameter = ring * 2 + 1

#     v       ^       v       ^       v       ^       v       ^
# 1   0   1   2   1   0   1   2   1   0   1   2   1   0   1   2
# 10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25

#         v           ^           v           ^           v           ^           v           ^
# 2   1   0   1   2   3   2   1   0   1   2   3   2   1   0   1   2   3   2   1   0   1   2   3
# 26  27  28  29  30  31  32  33  34  35  36  27  38  39  40  41  42  43  44  45  46  47  48  49

#         v           ^           v           ^           v           ^           v           ^
# 2   1   0   1   2   3   2   1   0   1   2   3   2   1   0   1   2   3   2   1   0   1   2   3
# 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23
#         2                       8                       14                      20


def p1(n):
    # I spent some time thinking about this one until I worked out how to turn it into a closed-form expression
    if n == 1:
        return 0
    ring = ceil(sqrt(n)) // 2
    diameter = ring * 2 + 1
    inner_sq = (diameter - 2) ** 2
    offset = abs(((n - inner_sq - 1) % (diameter - 1)) - ring + 1)
    return ring + offset


def p2():
    # Not so sure a closed-form expression is possible this time...
    grid = {(0, 0): 1}
    pos = (0, 0)
    order = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    heading = 0
    while True:
        pos = vadd(pos, order[heading])
        acc = 0
        for x in range(pos[0] - 1, pos[0] + 2):
            for y in range(pos[1] - 1, pos[1] + 2):
                if (x, y) in grid:
                    acc += grid[(x, y)]
        if acc > data:
            return acc
        grid[pos] = acc
        if vadd(pos, order[heading - 3]) not in grid:
            heading = (heading + 1) % 4
        # print_2d('    ', grid)


setday(3)

data = parselines(get_ints)[0][0]

assert p1(1) == 0
assert p1(12) == 3
assert p1(23) == 2
assert p1(1024) == 31

print('part1:', p1(data))
print('part2:', p2())
