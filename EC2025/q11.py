from ec import *


def p1():
    data = [x[0] for x in parse_lines(1, get_ints)]

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

    return


def p2():
    data = [x[0] for x in parse_lines(2, get_ints)]
    print(data)

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

    print(data, round_counter)
    return

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


def p2_fast():
    data = [x[0] for x in parse_lines(4, get_ints)]
    data_original = data.copy()

    round_counter = 0

    did_work = True
    while did_work:
        did_work = False
        for i in range(len(data)-1):
            j = 1
            # print('checking', i, data[i])
            while (i+j) < len(data) and data[i + j - 1] > data[i + j]:
                # print(i, j, data[i], data[j])
                j += 1
            if j == 1:
                continue
            did_work = True
            # print('range', data[i:i+j])
            sum_of_range = sum(data[i:i+j])
            # print('sum:', sum_of_range)
            d, m = sum_of_range//j, sum_of_range%j
            # print(f'd,m {d,m}')
            round_counter += max(data[i:i+j]) - min(data[i:i+j])
            for k in range(i, i+j):
                # print('changed', data[k], 'to', d)
                data[k] = d
            for k in range(i+j-m, i+j):
                data[k] += 1
                # print('added', 1, 'to', data[k], 'at index', k)

        # input()
    print(data, data_original)

    # round_counter = sum(b-a for a,b in zip(data, data_original) if b-a > 0)

    return round_counter



def p2_faster():
    data = [x[0] for x in parse_lines(4, get_ints)] # just the input parsed into a list

    round_counter = 0
    did_work = True

    while did_work:
        last_state = data.copy()
        did_work = False
        for i in range(len(data)-1):
            j = 1
            while (i+j) < len(data) and data[i + j - 1] > data[i + j]:
                j += 1
            if j == 1:
                continue
            did_work = True

            sum_of_range = sum(data[i:i+j])

            q, m = sum_of_range // j, sum_of_range % j

            this_change = max(data[i:i + j]) - min(data[i:i + j])
            # print(this_change)

            for k in range(i, i+j):
                data[k] = q
            for k in range(i+j-m, i+j):
                data[k] += 1
        diffs = [a-b for a,b in zip(data, last_state)]
        change = sum(i for i in diffs if i > 0)
        print(diffs, change)
        round_counter += change

    print(data, round_counter)


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

# 2795100
# 7696326

# print('part1:', p1())
# print('part2:', p2())
print('part2:', p2_faster())
# print('part3:', p3())
