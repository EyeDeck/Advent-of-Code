from ec import *


def solve(n):
    data = parse_lines(n)
    acc = 0
    for line in data:
        alloys = defaultdict(set)

        for cmp in line.split(' '):
            if cmp[1] == '<':
                alloys[cmp[0]].add(cmp[2])
                alloys[cmp[2]]
            else:
                alloys[cmp[0]]
                alloys[cmp[2]].add(cmp[0])

        order = {}
        while alloys:
            for alloy, weaker in alloys.items():
                if weaker.issubset(order):
                    order[alloy] = None
                    alloys.pop(alloy)
                    break

        acc += int(''.join(order.keys()))
    return acc



if __name__ == '__main__':
    setquest(2)

    print('part1:', solve(1))
    print('part2:', solve(2))
    print('part3:', solve(3))
