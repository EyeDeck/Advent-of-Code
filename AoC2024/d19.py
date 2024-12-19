from aoc import *


def p1():
    def get_neighbors(pattern, index):
        # print('\tcalled', pattern, index)
        potential_neighbors = set(pattern[index:index+i+1] for i in range(longest_towel))
        # print('\tpossible', potential_neighbors)
        neighbors = [(index+len(n), n) for n in potential_neighbors if n in towels]
        # print('\treturning', neighbors)
        return neighbors

    longest_towel = max(len(t) for t in towels)
    acc = 0
    for pattern in patterns:
        print(pattern)
        pattern_length = len(pattern)
        start = get_neighbors(pattern, 0)
        # print(start)

        q = deque(start)

        parent = {}

        while q:
            # print('q', q)
            length, cur = q.popleft()
            # print('l,c', length, cur)
            if length == pattern_length:
                acc += 1
                # print('\tpossible')
                break

            for (nlength, n) in get_neighbors(pattern, length):
                # print('rval', nlength, n)
                if (nlength, n) in parent:
                    continue
                parent[(nlength, n)] = cur
                q.append((nlength, n))


    return acc


def p2():
    @memo
    def solve(pattern):
        print(pattern)
        if pattern == '':
            return 1

        acc = 0
        for t in towels:
            if pattern.startswith(t):
               acc += solve(pattern[len(t):])
        return acc

    acc = 0
    for pattern in patterns:
        s = solve(pattern)
        print(s)
        acc += s
    return acc



setday(19)

with open_default() as file:
    towels, patterns = file.read().strip().split('\n\n')
towels = set(towels.split(', '))
patterns = patterns.split('\n')
print(towels)
print(patterns)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1() )
print('part2:', p2() )
