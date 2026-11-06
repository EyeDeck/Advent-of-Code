from ec import *


def p1():
    data = parse_lines(1)

    acc = 0
    for line in data:
        id, growth, limit = [int(x.split('=')[1].strip(',')) for x in line.split(' ')]

        if limit == 1:
            acc += 1
            continue

        branches = defaultdict(int, {1: 1})
        splits = 0
        second = 1
        while True:
            second += 1
            branches = defaultdict(int, {k+1:v for k,v in branches.items()})
            if growth in branches:
                splits += branches[growth]
                branches[1] += branches[growth]
                branches[growth//2] += branches[growth]*2
                branches.pop(growth)
            elements = splits + sum(k*v for k,v in branches.items())

            if elements >= limit:
                acc += second
                break

    return acc


def p2(part):
    data = parse_lines(part)

    acc = 0
    for line in data:
        id, growth, limit = [int(x.split('=')[1].strip(',')) for x in line.split(' ')]

        if limit == 1:  #FUCK
            acc += 1
            continue

        branches = defaultdict(int, {1: 1})
        splits = 0
        second = 1
        while True:
            longest_branch = max(branches.keys())
            dist_to_branch = growth - longest_branch
            second += dist_to_branch
            branches = defaultdict(int, {k+dist_to_branch:v for k,v in branches.items()})

            if growth in branches:
                splits += branches[growth]
                branches[1] += branches[growth]
                branches[growth//2] += branches[growth]*2
                branches.pop(growth)

            if (splits+1) >= limit:
                acc += second
                break

    return acc


if __name__ == '__main__':
    setquest(9)

    print('part1:', p1())
    print('part2:', p2(2))
    print('part3:', p2(3))
