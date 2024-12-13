import z3

from aoc import *


def p1():
    def wbfs(src, tgt, edges):
        """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
        a list of `(node, cost)` pairs."""
        q = [(0, src, None)]

        parent = {}

        while q:
            cost, cur, prev = heapq.heappop(q)
            if cur[0] > tgt[0] or cur[1] > tgt[1]:
                continue
            if cur in parent:
                continue
            parent[cur] = prev
            if cur == tgt:
                return cost

            for (n, ncost) in edges(cur):
                # print(cost, n, ncost)
                if n in parent:
                    continue
                heapq.heappush(q, (cost + ncost, n, cur))

        if tgt not in parent:
            return 0

        pos = tgt
        path = []
        while pos != src:
            path.append(pos)
            pos = parent[pos]
        path.append(src)
        path.reverse()
        return path

    def edge_func(cur):
        return (vadd(cur, a), 3), (vadd(cur, b), 1)

    acc = 0
    for line in data:
        a_x, a_y, b_x, b_y, prize_x, prize_y = line
        a = (a_x, a_y)
        b = (b_x, b_y)
        prize = (prize_x, prize_y)
        acc += wbfs((0, 0), prize, edge_func)

    return acc


def p1_2():
    def find_cost(a, b, prize):
        for i in range(100):
            for j in range(100):
                this_combination = vadd(vmul(a, (i, i)), vmul(b, (j, j)))
                # print(this_combination, prize)
                if this_combination == prize:
                    return i * 3 + j
        return 0

    acc = 0
    for line in data:
        a_x, a_y, b_x, b_y, prize_x, prize_y = line
        a = (a_x, a_y)
        b = (b_x, b_y)
        prize = (prize_x, prize_y)
        acc += find_cost(a, b, prize)

    return acc


def z3_this_nonsense(a, b, prize):
    optimizer = z3.Optimize()

    x, y = z3.Ints('x y')

    eq1 = a[0] * x + b[0] * y == prize[0]
    eq2 = a[1] * x + b[1] * y == prize[1]

    optimizer.add(eq1, eq2)

    optimizer.minimize(y)

    if optimizer.check() == z3.sat:
        solution = optimizer.model()
        return solution[x].as_long() * 3 + solution[y].as_long()
    else:
        return 0


def p2():
    acc = 0
    offset = 10000000000000
    for line in data:
        a_x, a_y, b_x, b_y, prize_x, prize_y = line
        a, b, prize = (a_x, a_y), (b_x, b_y), (prize_x+offset, prize_y+offset)
        acc += z3_this_nonsense(a, b, prize)
    return acc


setday(13)

data = parselines()
# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

with open_default() as file:
    data = [get_ints(line) for line in file.read().split('\n\n')]

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1() )
print('part1:', p1_2() )
print('part2:', p2() )

# print('part1: %d\npart2: %d' % solve())
