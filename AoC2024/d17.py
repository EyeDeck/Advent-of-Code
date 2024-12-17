from aoc import *


def get_output(a,b,c,program):
    def combo(op):
        if op <= 3:
            return op
        elif op == 4:
            return a
        elif op == 5:
            return b
        elif op == 6:
            return c
        elif op == 7:
            assert op != 7

    pointer = 0
    output = []

    while True:
        # if verbose:
        #     print(a,b,c,pointer)
        try:
            instruction, operand = program[pointer:pointer+2]
        except ValueError:
            break

        if instruction == 0:  # adv
            a = int(a / 2**combo(operand))
        elif instruction == 1:  # bxl
            b = b ^ operand
        elif instruction == 2:  # bst
            b = combo(operand) % 8
        elif instruction == 3:  # jnz
            if a != 0:
                pointer = operand - 2
        elif instruction == 4:  # bxc
            b = b ^ c
        elif instruction == 5:  # out
            # if verbose:
            #     print('out', operand, '=', combo(operand) % 8)
            output.append(combo(operand) % 8)
        elif instruction == 6:  # bdv
            b = int(a / 2 ** combo(operand))
        elif instruction == 7:  # cdv
            c = int(a / 2 ** combo(operand))

        pointer += 2

    return output


def p1():
    a,b,c = [i[0] for i in data[0:3]]
    program = data[4]
    return ','.join(str(i) for i in get_output(a,b,c,program))


def p2():
    a, b, c = [i[0] for i in data[0:3]]
    program = data[4]

    i = 0
    while True:
        ans = get_output(i, b, c, program)
        if verbose:
            print(oct(i), ans, len(ans))
        if ans == program:
            return i
        if ans == program[-len(ans):]:
            i *= 8
        else:
            i += 1


setday(17)

data = parselines(get_ints)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1() )
print('part2:', p2() )
