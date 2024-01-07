from aoc import *

class Node:
    def __init__(self, number, presents):
        self.number = number
        self.presents = presents
        self.next = None

def p1():
    elves = [Node(1, 1)]
    for i in range(data-1):
        elf = Node(i+2, 1)
        last_elf = elves[-1]
        last_elf.next = elf
        elves.append(elf)
    elves[-1].next = elves[0]

    elf = elves[0]
    while elf.next != elf:
        next_elf = elf.next
        elf.presents += next_elf.presents
        next_elf.presents = 0

        later_elf = elf.next.next
        elf.next = later_elf

        elf = later_elf
    return elf.number

def p2():
    elves = [[1, i+1] for i in range(data)]
    a, b = deque(elves[:data//2]), deque(elves[data//2:])
    toggle = data & 1
    while a and b:
        a[0][0] += b.popleft()[0]

        if toggle:
            a.append(b.popleft())
        toggle = not toggle

        b.append(a.popleft())

    return b.pop()[1]

setday(19)

data = int(parselines()[0])

print('part1:', p1() )
print('part2:', p2() )
