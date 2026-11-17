from ec import *


def p1():
    data = [c for c in parse_lines(1)[0]]

    acc = 0
    ln = len(data)
    l_pointer = 0
    r_pointer = ln - 1
    while True:
        c = data[l_pointer]

        while data[l_pointer] == c:
            l_pointer += 1

            if l_pointer >= r_pointer:
                return acc

        while data[r_pointer] != c:
            r_pointer -= 1
        else:
            r_pointer -= 1

        if r_pointer <= l_pointer:
            # l_pointer += 1
            r_pointer = ln - 1
            continue

        r_pointer += 1


        print(''.join(data), l_pointer, r_pointer, )
        dbg = [' ' for _ in range(ln)]
        dbg[l_pointer] = '-'
        dbg[r_pointer] = '+'

        print(''.join(dbg), c)
        data[l_pointer:r_pointer+1] = reversed(data[l_pointer:r_pointer+1])
        print(''.join(data))

        acc += 1


def p2():
    data = [c for c in parse_lines(2)[0]*10]

    acc = 0
    ln = len(data)
    l_pointer = 0
    r_pointer = ln - 1
    while True:
        c = data[l_pointer]

        while data[l_pointer] == c:
            l_pointer += 1

            if l_pointer >= r_pointer:
                return acc

        while data[r_pointer] != c:
            r_pointer -= 1
        else:
            r_pointer -= 1

        if r_pointer <= l_pointer:
            r_pointer = ln - 1
            continue

        r_pointer += 1

        data[l_pointer:r_pointer+1] = reversed(data[l_pointer:r_pointer+1])

        acc += r_pointer - l_pointer + 1


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
            # print(f'i am {self.index} and I am in mode {self.dir_state}, therefore I will yield _prev ({"None" if self._prev is None else self._prev.index})')
            return self._prev
        else:
            # print(f'i am {self.index} and I am in mode {self.dir_state}, therefore I will yield _next ({"None" if self._next is None else self._next.index})')
            return self._next

    @next.setter
    def next(self, val):
        if self.dir_state == 0 and not self.dir_holder[0]:
            # print(f'  node i {self.index} _next (_prev!) set to {val} ({val.index if val else "None"})')
            self._prev = val
        else:
            # print(f'  node i {self.index} _next set to {val} ({val.index if val else "None"})')
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




def p3():
    dir_holder = [True]
    # data = [Node(c, i,0, dir_holder) for i, c in enumerate(parse_lines(3)[0]*1)]
    data = [Node(c, i,0, dir_holder) for i, c in enumerate((parse_lines(3)[0]*100)+'x')]  # the x is load-bearing

    data[0].next = data[1]
    data[-1].prev = data[-2]
    for i, n in enumerate(data[1:-1]):
        n.prev = data[i]
        n.next = data[i+2]
        # n.data = n.data + str(i)

    # print(data)
    # print([(n.prev, n, n.next) for n in data])

    start_node = data[0]  # thankfully this one is always fixed

    acc = 0
    l_pointer, r_pointer = data[0], data[-1]
    l_index, r_index = 0, len(data) - 1

    while True:
        c = l_pointer.data

        while l_pointer.data == c:
            # print(f'-> {l_pointer}, (index {l_pointer.index}) (i {l_index})')
            l_pointer.dir_state, l_pointer.next, l_pointer.prev = 1, l_pointer.next, l_pointer.prev
            l_pointer = l_pointer.next
            # n, p = l_pointer.next, l_pointer.prev
            # l_pointer.dir_state = 1
            # l_pointer.next, l_pointer.prev = n, p
            # l_pointer = n

            if l_pointer is data[-1]:
                return acc

            l_index += 1

            # input()

            # if r_pointer == l_pointer:
            #     return acc

        # print(f'STOPPED left node on l_pointer: {l_pointer},{l_pointer.index} ({l_pointer.prev},{l_pointer},{l_pointer.next})')

        # l_pointer = l_pointer.next
        # l_index += 1

        while r_pointer.data != c:
            # print(f'<- {r_pointer}, (index {r_pointer.index}) (i {r_index})')
            r_pointer.dir_state, r_pointer.next, r_pointer.prev = 1, r_pointer.next, r_pointer.prev
            r_pointer = r_pointer.prev
            # n, p = r_pointer.next, r_pointer.prev
            # r_pointer.dir_state = 1
            # r_pointer.next, r_pointer.prev = n, p
            # r_pointer = p
            r_index -= 1

            # input()

            if r_index <= l_index:
                break

        if r_index <= l_index:
            print('TRIPPED CONTINUE STATE')

            while True:
                nxt = r_pointer.next
                r_pointer.normalize()

                if nxt is None:
                    break

                r_pointer = nxt

            dir_holder[0] = True
            r_index = len(data) - 1

            continue


        # print(f'STOPPED right node on r_pointer: {r_pointer},{r_pointer.index} ({r_pointer.prev},{r_pointer},{r_pointer.next})')
        # print('BUILDING DBG')
        #
        # srt = [start_node]
        # while srt[-1].next:
        #     # print(srt[-1].index)
        #     assert srt[-1].next not in srt
        #     srt.append(srt[-1].next)
        #
        # print(''.join([n.data for n in srt]), l_index, r_index)
        # dbg = [' ' for _ in range(len(srt))]
        # dbg[l_index] = '-'
        # dbg[r_index] = '+'
        # print(''.join(dbg), c)

        # print(f'l_pointer: {l_pointer},{l_pointer.index}, r_pointer: {r_pointer},{r_pointer.index} | ({l_pointer.prev},{l_pointer},{l_pointer.next}) ({r_pointer.prev},{r_pointer},{r_pointer.next})')

        # data[l_pointer:r_pointer+1] = reversed(data[l_pointer:r_pointer+1])

        # acc += r_pointer - l_pointer + 1

        # l_pointer.prev.next, r_pointer.next.prev, r_pointer.next, l_pointer.prev, r_pointer, l_pointer = r_pointer, l_pointer, l_pointer.prev, r_pointer.next, r_pointer.next, l_pointer.prev
        l_pointer.prev.next, r_pointer.next.prev, r_pointer.next, l_pointer.prev = r_pointer, l_pointer, l_pointer.prev, r_pointer.next

        l_pointer, r_pointer, = r_pointer, l_pointer

        dir_holder[0] = not dir_holder[0]


        # print('REBUILDING DBG')
        # srt = [start_node]
        # while srt[-1].next:
        #     # print(srt[-1].index)
        #     assert srt[-1].next not in srt
        #     srt.append(srt[-1].next)

        # print(''.join([n.data for n in srt]), l_index, r_index)
        # dbg = [' ' for _ in range(len(srt))]
        # dbg[l_index] = '-'
        # dbg[r_index] = '+'
        # print(''.join(dbg), c)


        # input()

        acc += r_index - l_index + 1
        # acc += 1

# RRGGBBGRRGGBBG 2 8
#   -     +      R


def p3x():
    data = [c for c in parse_lines(3)[0]*1]

    print(''.join(data))

    acc = 0
    ln = len(data)
    l_pointer = 0
    r_pointer = ln - 1
    flipped = False
    while True:
        c = data[l_pointer]

        if not flipped:
            while data[l_pointer] == c:
                l_pointer += 1

                if l_pointer >= r_pointer:
                    return acc

            while data[r_pointer] != c:
                r_pointer -= 1
            r_pointer -= 1

            r_pointer2 = r_pointer
            while data[r_pointer2-1] == c:
                r_pointer2 -= 1

            if r_pointer <= l_pointer:
                r_pointer = ln - 1
                continue

            r_pointer += 1

            right_len = r_pointer-r_pointer2+1

            data[l_pointer:l_pointer+right_len], data[r_pointer2:r_pointer2+right_len] = data[r_pointer2:r_pointer2+right_len], data[l_pointer:l_pointer+right_len]

            acc += r_pointer - l_pointer + 1

            # data[l_pointer:r_pointer+1] = reversed(data[l_pointer:r_pointer+1])
            print(''.join(data), l_pointer, r_pointer, r_pointer2, ',', right_len)
            dbg = [' ' for _ in range(ln)]
            dbg[l_pointer] = '-'
            dbg[r_pointer] = '+'
            dbg[r_pointer2] = '~'
            print(''.join(dbg), c)
            data[l_pointer:r_pointer + 1] = reversed(data[l_pointer:r_pointer + 1])
            print(''.join(data))

            l_pointer += right_len
            r_pointer -= right_len

            dbg = [' ' for _ in range(ln)]
            dbg[l_pointer] = '-'
            dbg[r_pointer] = '+'
            dbg[r_pointer2] = '~'
            print(''.join(dbg), c, '?')




if __name__ == '__main__':
    setquest(16)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
