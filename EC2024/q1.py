from collections import Counter

from ec import *


def p1():
    data = parse_lines(1)[0]
    pmap = {'A': 0, 'B': 1, 'C': 3}
    return sum(pmap[c] for c in data)


def p2():
    data = parse_lines(2)[0]
    pmap = {'A': 0, 'B': 1, 'C': 3, 'D': 5, 'x':0}
    acc = 0
    for i in range(0, len(data), 2):
        chunk = data[i:i+2]
        if chunk == 'xx':
            continue
        if 'x' not in chunk:
            acc += 2
        acc += pmap[chunk[0]] + pmap[chunk[1]]
    return acc


def p3():
    data = parse_lines(3)[0]
    pmap = {'A': 0, 'B': 1, 'C': 3, 'D': 5, 'x':0}
    acc = 0
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        counts = Counter(chunk)
        if counts['x'] == 3:
            continue
        extra = (2-counts['x']) * (3-counts['x'])
        acc += sum(pmap[chunk[j]] for j in range(3)) + extra
    return acc


if __name__ == '__main__':
    setquest(1)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
