from ec import *


def p1():
    names, instructions = [x.split(',') for x in parsedouble(1)]
    name_len = len(names)
    name_max = name_len - 1

    pointer = 0
    for ins in instructions:
        dir, offset = ins[0], int(ins[1:])
        if dir == 'L':
            pointer = max(pointer - offset, 0)
        elif dir == 'R':
            pointer = min(pointer + offset, name_max)
    return names[pointer]


def p2():
    names, instructions = [x.split(',') for x in parsedouble(2)]
    name_len = len(names)

    pointer = 0
    for ins in instructions:
        dir, offset = ins[0], int(ins[1:])
        if dir == 'L':
            pointer = (pointer - offset) % name_len
        elif dir == 'R':
            pointer = (pointer + offset) % name_len
        # print(dir, offset, pointer, names[pointer])
    return names[pointer]


def p3():
    names, instructions = [x.split(',') for x in parsedouble(3)]
    name_len = len(names)

    for ins in instructions:
        pointer = 0
        dir, offset = ins[0], int(ins[1:])
        if dir == 'L':
            pointer = (pointer - offset) % name_len
        elif dir == 'R':
            pointer = (pointer + offset) % name_len
        names[0], names[pointer] = names[pointer], names[0]
        # print(names)
    return names[0]


setquest(1)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
