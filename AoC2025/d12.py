
from aoc import *

def p1():
    acc = 0
    for box, counts in boxes:
        total_ct = 0
        for i, ct in enumerate(counts):
            total_ct += len(shapes[i]) * ct

        print(total_ct, math.prod(box))

        if total_ct > math.prod(box):
            print('skipped')
            continue
        acc += 1
    return acc


def p2():
    return None


if __name__ == '__main__':
    setday(12)

    with open_default() as file:
        data = file.read().split('\n\n')

    shapes = []
    for shape_raw in data[:-1]:
        shape = []
        for y, line in enumerate(shape_raw.split('\n')[1:]):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    shape.append((x,y))
        print(shape)
        shapes.append(shape)

    for shape in shapes:
        print_2d('  ', {k: '#' for k in shape})
        print()

    print(shapes)

    boxes = []
    for box_raw in data[-1].split('\n'):
        ints = get_ints(box_raw)
        boxes.append((tuple(ints[0:2]), tuple(ints[2:]), ))
    print(boxes)

    print('part1:', p1() )
    print('part2:', p2() )
