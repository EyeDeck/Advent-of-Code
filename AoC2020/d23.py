import sys


class Node:
    def __init__(self, v=None):
        self.v = v
        self.n = None


def get_len_at_starting(length, s, nodes):
    p = []
    nx = nodes[s]
    for i in range(length):
        p.append(nx.v)
        nx = nx.n
    return p


def val_is_in_next(val, ct, node):
    for _ in range(ct):
        if val == node.v:
            return True
        node = node.n
    return False


def solve_for(cups, iterations):
    min_cup = min(cups)
    max_cup = max(cups)

    nodes = [None for _ in range(max_cup+1)]
    last = None
    for c in cups:
        new = Node(c)
        if last is not None:
            last.n = new
        nodes[c] = new
        last = new

    current_id = cups[0]
    current = nodes[current_id]
    last.n = current

    for move in range(iterations):
        # relink third index ahead to 'current'
        start_rmv = current.n
        end_rmv = start_rmv.n.n
        post_rmv = end_rmv.n
        current.n = post_rmv

        # select destination
        dest_id = current_id - 1
        if dest_id < min_cup:
            dest_id = max_cup
        while val_is_in_next(dest_id, 3, start_rmv):
            dest_id -= 1
            if dest_id < min_cup:
                dest_id = max_cup
        dest = nodes[dest_id]

        # reinsert removed 3 at appropriate index
        end_rmv.n = dest.n
        dest.n = start_rmv

        # increment cup
        current_id = current.n.v
        current = nodes[current_id]

    return nodes


def p1():
    result = solve_for(data, 100)
    return ''.join(str(i) for i in get_len_at_starting(len(data), 1, result)[1:])


def p2():
    data2 = data.copy()
    data2.extend([i for i in range(max(data2)+1, 1_000_001)])
    result = solve_for(data2, 10_000_000)
    return result[1].n.v * result[1].n.n.v


starting = "952438716"
if len(sys.argv) > 2:
    n, moves = sys.argv[1], sys.argv[2]

data = [int(i) for i in starting]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
