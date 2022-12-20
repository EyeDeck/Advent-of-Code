import sys


class Node:
    def __init__(self, prev, d, next=None):
        self.prev = prev
        self.d = d
        self.next = next


def get_offset(node, ct, ln):
    ct %= ln
    if ct < 0:
        for _ in range(-ct + 1):
            node = node.prev
    else:
        for _ in range(ct):
            node = node.next
    return node


def print_ll(v0, ll):
    p = v0
    for i in range(len(ll) + 1):
        print(p.d, end=' ')
        p = p.next
    print('\n')


def shuffle(ll, data_len):
    for node in ll:
        d = node.d
        if d == 0:
            continue

        # note that we have to pop the node from the list BEFORE getting the offset,
        # otherwise we can loop back over the starting number and throw it all off
        current_left, current_right = node.prev, node.next
        current_left.next = current_right
        current_right.prev = current_left

        offset = get_offset(node, node.d, data_len)

        next_left, next_right = offset, offset.next

        node.prev = next_left
        node.next = next_right

        next_left.next = node
        next_right.prev = node

    return ll


def make_ll(d, m=1):
    v0 = None
    ll = [Node(None, d[0] * m)]
    for line in d[1:]:
        next_node = Node(ll[-1], line * m, None)
        ll[-1].next = next_node
        ll.append(next_node)
        if line == 0:
            v0 = ll[-1]
    ll[-1].next = ll[0]
    ll[0].prev = ll[-1]
    return v0, ll


def solve(data, shuffles, mult):
    v0, ll = make_ll(data, mult)
    for i in range(shuffles):
        shuffle(ll, len(data) - 1)
    acc = 0
    for i in range(3):
        v0 = get_offset(v0, 1000, len(data))
        acc += v0.d
    return acc


day = 20
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [int(line) for line in file]

print('part1:', solve(data, 1, 1))
print('part1:', solve(data, 10, 811589153))
