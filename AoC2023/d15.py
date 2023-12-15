from aoc import *


def p1():
    acc = 0
    for step in data:
        curr = 0
        for char in step:
            curr += ord(char)
            curr *= 17
            curr %= 256
        acc += curr
    return acc


def p2():
    lightboxes = [{} for _ in range(256)]
    for step in data:
        if step[-1] == '-':
            label = step[:-1]
            op = '-'
        else:
            label = step[:-2]
            op = int(step[-1])

        curr = 0
        for char in label:
            curr += ord(char)
            curr *= 17
            curr %= 256

        if op == '-':
            if label in lightboxes[curr]:
                del lightboxes[curr][label]
        else:
            lightboxes[curr][label] = op

    acc = 0
    for i, box in enumerate(lightboxes):
        for j, (lens, v) in enumerate(box.items()):
            acc += (1+i) * (j+1) * v

    return acc


setday(15)

data = parselines()
data = [word for word in data[0].strip().split(',')]

print('part1:', p1() )
print('part2:', p2() )
