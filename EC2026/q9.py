from ec import *


def p1():
    data = parse_lines(1)

    acc = 0
    for line in data:
        id, growth, limit = [int(x.split('=')[1].strip(',')) for x in line.split(' ')]
        print(id, growth, limit)
        branches = defaultdict(int, {1: 1})
        splits = 0
        for second in range(2,1_000_000):
            branches = defaultdict(int, {k+1:v for k,v in branches.items()})
            if growth in branches:
                splits += branches[growth]
                branches[1] += branches[growth]
                branches[growth//2] += branches[growth]*2
                branches.pop(growth)
            elements = splits + sum(k*v for k,v in branches.items())
            print(branches)
            print(f'sec:{second}, elem{elements}, splits:{splits}')

            if elements >= limit:
                acc += second
                break

    return acc


def p2():
    data = parse_lines(2)

    acc = 0
    for line in data:
        id, growth, limit = [int(x.split('=')[1].strip(',')) for x in line.split(' ')]
        print(id, growth, limit)
        branches = defaultdict(int, {1: 1})
        splits = 0
        for second in range(2,1_000_000):
            branches = defaultdict(int, {k+1:v for k,v in branches.items()})
            if growth in branches:
                splits += branches[growth]
                branches[1] += branches[growth]
                branches[growth//2] += branches[growth]*2
                branches.pop(growth)
            elements = splits + sum(k*v for k,v in branches.items())
            print(branches)
            print(f'sec:{second}, elem{elements}, splits:{splits}')

            if (splits+1) >= limit:
                acc += second
                break

    return acc


def p3():
    data = parse_lines(3)

    acc = 0
    for line in data:
        id, growth, limit = [int(x.split('=')[1].strip(',')) for x in line.split(' ')]
        # print(id, growth, limit)
        print(f'id:{id}, growth:{growth}, limit:{limit}')
        branches = defaultdict(int, {1: 1})
        splits = 0
        second = 1
        while True:
            longest_branch = max(branches.keys())
            dist_to_branch = growth - longest_branch
            print('longest', longest_branch, 'dist', dist_to_branch)
            second += dist_to_branch
            branches = defaultdict(int, {k+dist_to_branch:v for k,v in branches.items()})
            if growth in branches:
                splits += branches[growth]
                branches[1] += branches[growth]
                branches[growth//2] += branches[growth]*2
                branches.pop(growth)

            elements = splits + sum(k*v for k,v in branches.items())
            print(branches)
            print(f'sec:{second}, elem{elements}, splits:{splits}')

            if (splits+1) >= limit:
                print(f'sec:{second}, splits:{splits}\n')
                acc += second
                break

    return acc

#p3 849559434880984 not correct
#p3 849559434880884 also not correct
#   849559434880884
#   849559434880884

def p3():
    data = parse_lines(3)

    acc = 0
    for line in data:
        id, growth, limit = [int(x.split('=')[1].strip(',')) for x in line.split(' ')]
        print(id, growth, limit)
        branches = defaultdict(int, {1: 1})
        splits = 0
        second = 1
        if limit == 1:  #FUCK
            acc += 1
            continue

        while True:
            longest_branch = max(branches.keys())
            dist_to_branch = growth - longest_branch - 1
            print('longest', longest_branch, 'dist', dist_to_branch)
            second += dist_to_branch
            branches = defaultdict(int, {k+dist_to_branch:v for k,v in branches.items()})

            branches = defaultdict(int, {k+1:v for k,v in branches.items()})
            second += 1
            if growth in branches:
                splits += branches[growth]
                branches[1] += branches[growth]
                branches[growth//2] += branches[growth]*2
                branches.pop(growth)
            elements = splits + sum(k*v for k,v in branches.items())
            print(branches)
            print(f'sec:{second}, elem{elements}, splits:{splits}')

            if (splits+1) >= limit:
                acc += second
                break

    return acc


if __name__ == '__main__':
    setquest(9)

    # print('part1:', p1())
    # print('part2:', p2())
    print('part3:', p3())
