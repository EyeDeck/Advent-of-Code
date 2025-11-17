from ec import *


def p1():
    data = [x[0] for x in parse_lines(1, get_ints)]
    print(data, sum(data))
    round_counter = 0
    moved = True
    while moved:
        moved = False
        for i in range(len(data)-1):
            if data[i+1] < data[i]:
                data[i] -= 1
                data[i+1] += 1
                moved = True
        if moved:
            round_counter += 1
            if round_counter == 10:
                return sum((i + 1) * n for i, n in enumerate(data))


    print(data, sum(data), round_counter)

    moved = True
    while moved:
        round_counter += 1
        moved = False
        for i in range(len(data)-1):
            if data[i+1] > data[i]:
                data[i] += 1
                data[i+1] -= 1
                moved = True
        if moved:
            print(round_counter, data, sum(data))
            if round_counter == 10:
                return sum((i + 1) * n for i, n in enumerate(data))


    print(data, sum(data), round_counter)
    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)

    return


def p2():
    data = [x[0] for x in parse_lines(2, get_ints)]

    print(data, sum(data))
    round_counter = 0
    moved = True
    while moved:
        moved = False
        for i in range(len(data)-1):
            if data[i+1] < data[i]:
                data[i] -= 1
                data[i+1] += 1
                moved = True
        if moved:
            round_counter += 1

    moved = True
    while moved:
        moved = False
        for i in range(len(data)-1):
            if data[i+1] > data[i]:
                data[i] += 1
                data[i+1] -= 1
                moved = True
        if moved:
            round_counter += 1


    print(data, sum(data), round_counter)
    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)

    return round_counter


def p3():
    data = [x[0] for x in parse_lines(3, get_ints)]

    print(data, sum(data))
    round_counter = 0
    moved = True
    while moved:
        moved = False
        for i in range(len(data)-1):
            if data[i+1] < data[i]:
                data[i] -= 1
                data[i+1] += 1
                moved = True
        if moved:
            round_counter += 1

    end_ea = sum(data) // len(data)

    print(data, end_ea, round_counter)

    thing = [end_ea - n for n in data]
    print(thing, sum(n for n in thing if n > 0))

    return sum(n for n in thing if n > 0)


setquest(11)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
