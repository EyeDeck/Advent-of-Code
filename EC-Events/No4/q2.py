import random

from ec import *


def p1():
    data = parse_lines(1)
    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)
    # grid, inverse, unique = parse_grid()
    pos, a, b, c = [get_ints(x) for x in data[:4]]
    moves = data[4].split('=')[1]

    move_map = {'A':a, 'B':b, 'C':c}

    print(pos, a, b, c, moves)

    visited = {tuple(pos)}
    for move in moves:
        pos = vidiv(vadd(pos, move_map[move]), [2,2])
        visited.add(tuple(pos))
        print(pos, move)

    print_2d('.', {(x,-y):'#' for x,y in visited})
    return len(visited)


def p2():
    data = parse_lines(2)
    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)
    # grid, inverse, unique = parse_grid()
    pos, a, b, c = [get_ints(x) for x in data[:4]]
    moves = data[4].split('=')[1]

    move_map = {'A':a, 'B':b, 'C':c}

    # print(pos, a, b, c, moves)

    def get_midpoint(a,b):
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    visited = {tuple(pos)}
    for move in moves:
        # pos = vidiv(vadd(pos, move_map[move]), [2,2])
        pos = get_midpoint(pos, move_map[move])
        visited.add(tuple(pos))
        # print(pos, move)

    visited_adj = set()
    for firefly in visited:
        for dir in DIRS:
            p = tuple(vadd(firefly, dir))
            if p in visited:
                continue
            visited_adj.add(p)

    print_2d('.', {(x,-y):'#' for x,y in visited})
    print_2d('.', {(x,-y):'F' for x,y in visited_adj}, {(x,-y):'X' for x,y in visited})
    return len(visited_adj)


def p3():
    data = parse_lines(3)
    pos, a, b, c = [get_ints(x) for x in data[:4]]

    move_map = {'A':a, 'B':b, 'C':c}

    print(pos, a, b, c)

    visited = {tuple(pos)}
    for iteration in range(1_000_000):
        move = random.choice('ABC')
        pos = vidiv(vadd(pos, move_map[move]), [2,2])
        visited.add(tuple(pos))

    visited_adj = set()
    for firefly in visited:
        for dir in DIRS:
            p = tuple(vadd(firefly, dir))
            if p in visited:
                continue
            visited_adj.add(p)

    print_2d('.', {(x,-y):'#' for x,y in visited})
    # print_2d('.', {(x,-y):'F' for x,y in visited_adj}, {(x,-y):'X' for x,y in visited})
    return len(visited_adj)


def p3_fixed():
    data = parse_lines(3)
    start, a, b, c = [tuple(get_ints(x)) for x in data[:4]]

    print(start, a, b, c)

    def get_midpoint(a,b):
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    visited = {start,}
    stack = [start,]

    while stack:
        cur = stack.pop()
        neighbors = [get_midpoint(cur, a), get_midpoint(cur, b), get_midpoint(cur, c)]

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    visited_adj = set()
    for firefly in visited:
        for dir in DIRS:
            p = tuple(vadd(firefly, dir))
            if p in visited:
                continue
            visited_adj.add(p)

    print_2d('.', {(x,-y):'#' for x,y in visited})
    print_2d('.', {(x,-y):'F' for x,y in visited_adj}, {(x,-y):'X' for x,y in visited})
    return len(visited_adj)


setquest(2)

# print('part1:', p1())
print('part2:', p2())
# print('part3:', p3())
print('part3:', p3_fixed())

#17210 (100m) still wrong
# Your answer length is: correct
# The first character of your answer is: correct
