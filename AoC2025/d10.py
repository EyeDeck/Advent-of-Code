from aoc import *

import z3


def p1():
    acc = 0
    for line in data:
        sp = line.split()
        indicator = sum((1 if s =='#' else 0) << i for i,s in enumerate(sp[0].strip('[]')))
        buttons = [sum(1 << i for i in get_ints(s)) for s in sp[1:-1]]
        # joltage = get_ints(sp[-1])

        # print(bin(indicator), [bin(i) for i in buttons], joltage)
        # print(2**len(buttons))

        best = INF
        for i in range(1, 2 ** len(buttons)):
            split_bin = [int(s) for s in bin(i)[2:].zfill(len(buttons))]
            # print('', i, bin(i), split_bin)

            toggles = [buttons[button_index] for button_index, to_press in enumerate(split_bin) if to_press == 1]
            # print('\t', [i for i in toggles])

            state = 0
            for i in toggles:
                state ^= i

            if state == indicator:
                best = min(best, sum(split_bin))
        #         print('\t', split_bin)
        # print('best:', best)
        acc += best

    return acc


def p2():
    acc = 0
    for line in data:
        sp = line.split()
        joltages = get_ints(sp[-1])
        j_len = len(joltages)
        buttons_raw = sp[1:-1]
        buttons = [list(reversed([int(j) for j in bin(sum(1 << i for i in get_ints(s)))[2:].zfill(j_len)])) for s in buttons_raw]
        b_len = len(buttons)

        m = [z3.Int(f'm{i}') for i in range(len(buttons))]

        print('b,j', buttons, joltages)
        # print(m)

        opt = z3.Optimize()

        for multiplier in m:
            opt.add(multiplier >= 0)

        for j_i, joltage in enumerate(joltages):
            gen = (m[b_i] * buttons[b_i][j_i] for b_i in range(b_len))
            opt.add(z3.Sum(gen) == joltage)

        total = z3.Sum(m)

        print('assertions:', opt.assertions())

        opt.minimize(total)

        print(opt.check())
        model = opt.model()

        # print(opt.model()[total])
        presses = [model[multiplier].as_long() for multiplier in m]
        print(presses)
        acc += sum(presses)

    return acc


if __name__ == '__main__':
    setday(10)

    data = parselines()

    print('part2:', p2() )
