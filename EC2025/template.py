from ec import *


def p1():
    data = parse_lines(1)
    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)

    return


def p2():
    data = parse_lines(2)
    # data = parse_lines(2, get_ints)
    # data = parse_double_break(2)

    return


def p3():
    data = parse_lines(3)
    # data = parse_lines(3, get_ints)
    # data = parse_double_break(3)

    return


setquest()

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
