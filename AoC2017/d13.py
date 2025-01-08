from aoc import *


def p1():
    acc = 0
    for line in data:
        d, r = line
        if d % ((r - 1) * 2) == 0:
            acc += d * r
    return acc


def p2():
    if '-z3' in sys.argv or '--z3' in sys.argv:
        import z3

        optimizer = z3.Optimize()

        t = z3.Int('t')

        optimizer.add(t >= 0)

        for line in data:
            d, r = line
            eq = (d + t) % ((r - 1) * 2) != 0
            print(eq)
            optimizer.add(eq)

        optimizer.minimize(t)

        if optimizer.check() == z3.sat:
            solution = optimizer.model()
            return solution[t].as_long()

    else:
        i = 0
        while True:
            for line in data:
                d, r = line
                if (d + i) % ((r - 1) * 2) == 0:
                    break
            else:
                return i
            i += 1


setday(13)

data = sorted(parselines(get_ints), key=lambda x: x[1])

print('part1:', p1())
print('part2:', p2())
