from ec import *


def solve(part):
    def get_midpoint(a,b):
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    data = parse_lines(part)
    pos, a, b, c = [tuple(get_ints(x)) for x in data[:4]]
    visited = {pos,}
    stack = [pos,]

    if part <= 2:
        moves = data[4].split('=')[1]
        move_map = {'A': a, 'B': b, 'C': c}

        visited = {pos}
        for move in moves:
            pos = get_midpoint(pos, move_map[move])
            visited.add(pos)

    else:
        while stack:
            cur = stack.pop()
            neighbors = [get_midpoint(cur, a), get_midpoint(cur, b), get_midpoint(cur, c)]

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)

    if part == 1:
        return len(visited)

    visited_adj = set()
    for firefly in visited:
        for DIR in DIRS:
            p = tuple(vadd(firefly, DIR))
            if p in visited:
                continue
            visited_adj.add(p)

    if verbose:
        print_2d('.', {(x,-y):'#' for x,y in visited})
        print_2d('.', {(x,-y):'F' for x,y in visited_adj}, {(x,-y):'X' for x,y in visited})

    return len(visited_adj)

setquest(2)

print('part1:', solve(1))
print('part2:', solve(2))
print('part3:', solve(3))
