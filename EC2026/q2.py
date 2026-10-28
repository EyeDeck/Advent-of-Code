from ec import *


def solve(n):
    data = parse_lines(n)
    acc = 0
    for line in data:
        alloys = defaultdict(set)
        comparators = line.split(' ')
        # print(comparators)
        for c in comparators:
            if c[1] == '<':
                alloys[c[0]].add(c[2])
                alloys[c[2]] |= set()
            else:
                alloys[c[2]].add(c[0])
                alloys[c[0]] |= set()
        # print(alloys)
        # print(len(alloys['2']), len(alloys['3']))
        order_s = set()
        order_l = []
        while alloys:
            for alloy in alloys:
                if all(a in order_s for a in alloys[alloy]):
                    order_s.add(alloy)
                    order_l.append(alloy)
                    alloys.pop(alloy)
                    break
        # print(order_l)
        acc += int(''.join(order_l))
    return acc



if __name__ == '__main__':
    setquest(2)

    print('part1:', solve(1))
    print('part2:', solve(2))
    print('part3:', solve(3))
