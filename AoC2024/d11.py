from aoc import *


class Node:
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


def tick(stones):
    new_stones = []
    for stone in stones:
        n = stone.data
        s = str(n)
        if n == 0:
            stone.data = 1
        elif len(s) % 2 == 0:
            l, r = int(s[:len(s) // 2]), int(s[len(s) // 2:])
            stone.data = l
            r_stone = Node(r, stone, stone.next)
            # print(r_stone, r_stone.data, r_stone.prev, r_stone.next)
            new_stones.append(r_stone)
            if stone.next is not None:
                stone.next.prev = r_stone
            stone.next = r_stone
        else:
            stone.data *= 2024
    stones.extend(new_stones)


def p1():
    stones = [Node(i) for i in data]
    for i in range(len(stones[:-1])):
        stones[i].next = stones[i + 1]
    for i in range(len(stones[1:])):
        stones[i].prev = stones[i - 1]

    for tickct in range(1, 26):

        tick(stones)

        if verbose:
            print(f'{tickct}:', end='')
            stone = stones[0]
            while True:
                print(f'{stone.data} ', end='')
                if stone.next is None:
                    print()
                    break
                stone = stone.next
        else:
            print(f'{tickct}:{len(stones)}')

    return len(stones)


def p2():
    def tick(bins):
        new_bins = defaultdict(int)

        for stone, ct in bins.items():
            s = str(stone)
            if stone == 0:
                new_bins[1] += ct
            elif len(s) % 2 == 0:
                l, r = int(s[:len(s) // 2]), int(s[len(s) // 2:])

                new_bins[l] += ct
                new_bins[r] += ct

            else:
                new_bins[stone*2024] += ct

        return new_bins

    bins = defaultdict(int, {k:1 for k in data})

    for i in range(75):
        bins = tick(bins)

    return sum(bins.values())


setday(11)

with open_default() as file:
    data = [int(i) for i in file.read().strip().split(' ')]

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())
