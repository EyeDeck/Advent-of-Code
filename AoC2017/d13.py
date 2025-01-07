from aoc import *


def p1():
    acc = 0
    for line in data:
        d, r = line
        if d % ((r - 1) * 2) == 0:
            acc += d * r
    return acc


def p2_oops():
    def get_neighbors(a):
        index, delay = a
        d, r = data[index + 1]
        neighbors = []
        for i in range(50):
            if (d + delay + i) % ((r - 1) * 2) == 0:
                neighbors.append(((index + 1, delay + i), i))
        return neighbors

    def wbfs(src, edges):
        q = [(0, src, None)]

        parent = {}

        while q:
            # print(q)
            cost, cur, prev = heapq.heappop(q)
            if cur in parent:
                continue

            parent[cur] = prev
            # print(cur[0], len(data))
            if cur[0] == len(data) - 1:
                return cost

            for (n, ncost) in edges(cur):
                if n in parent:
                    continue
                heapq.heappush(q, (cost + ncost, n, cur))

    acc = 0
    for line in data:
        d, r = line
        if d % ((r - 1) * 2) == 0:
            acc += d * r
    return wbfs((0, 0), get_neighbors)


def p2():
    acc = 0
    for i in range(100_000_000):
        for line in data:
            d, r = line
            if (d + i) % ((r - 1) * 2) == 0:
                break
        else:
            return i
    return acc


setday(13)

data = parselines(get_ints)

print('part1:', p1())
print('part2:', p2())
print('part2:', p2_oops())
