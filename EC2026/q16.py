from ec import *


class Node:
    def __init__(self, data, index, dir_state, dir_holder, next=None, prev=None):
        self.data = data
        self.index = index
        self.dir_state = dir_state
        self.dir_holder = dir_holder
        self._next = next
        self._prev = prev

    def __repr__(self):
        return self.data

    @property
    def next(self):

        if self.dir_state == 0 and not self.dir_holder[0]:
            return self._prev
        else:
            return self._next

    @next.setter
    def next(self, val):
        if self.dir_state == 0 and not self.dir_holder[0]:
            self._prev = val
        else:
            self._next = val

    @property
    def prev(self):
        if self.dir_state == 0 and not self.dir_holder[0]:
            return self._next
        else:
            return self._prev

    @prev.setter
    def prev(self, val):
        if self.dir_state == 0 and not self.dir_holder[0]:
            self._next = val
        else:
            self._prev = val

    def normalize(self):
        self._next, self._prev, self.dir_state = self.next, self.prev, 0


def solve(part, mult):
    dir_holder = [True]

    # the x is load-bearing
    data = [Node(c, i, 0, dir_holder) for i, c in enumerate((parse_lines(part)[0] * mult) + 'x')]

    data[0].next = data[1]
    data[-1].prev = data[-2]
    for i, n in enumerate(data[1:-1]):
        n.prev = data[i]
        n.next = data[i + 2]

    flip_ct = 0
    flip_len = 0
    l_pointer, r_pointer = data[0], data[-1]
    l_index, r_index = 0, len(data) - 1

    while True:
        c = l_pointer.data

        while l_pointer.data == c:
            l_pointer.dir_state, l_pointer.next, l_pointer.prev = 1, l_pointer.next, l_pointer.prev
            l_pointer = l_pointer.next

            if l_pointer is data[-1]:
                return flip_ct, flip_len

            l_index += 1

        while r_pointer.data != c:
            r_pointer.dir_state, r_pointer.next, r_pointer.prev = 1, r_pointer.next, r_pointer.prev
            r_pointer = r_pointer.prev

            r_index -= 1

            if r_index <= l_index:
                break

        if r_index <= l_index:

            while True:
                nxt = r_pointer.next
                r_pointer.normalize()

                if nxt is None:
                    break

                r_pointer = nxt

            dir_holder[0] = True
            r_index = len(data) - 1

            continue

        l_pointer.prev.next, r_pointer.next.prev, r_pointer.next, l_pointer.prev = r_pointer, l_pointer, l_pointer.prev, r_pointer.next

        l_pointer, r_pointer, = r_pointer, l_pointer

        dir_holder[0] = not dir_holder[0]

        flip_ct += 1
        flip_len += r_index - l_index + 1


if __name__ == '__main__':
    setquest(16)

    print('part1:', solve(1, 1)[0])
    print('part2:', solve(2, 10)[1])
    print('part3:', solve(3, 100)[1])
