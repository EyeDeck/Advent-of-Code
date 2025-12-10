from aoc import *

import z3


def p1():
    acc = 0
    for line in data:
        sp = line.split()
        indicator = sum((1 if s == '#' else 0) << i for i, s in enumerate(sp[0].strip('[]')))
        buttons = [sum(1 << i for i in get_ints(s)) for s in sp[1:-1]]

        if verbose:
            print(f'\nTarget: {bin(indicator)}\nXOR values: {[bin(i) for i in buttons]}')

        best = INF
        for i in range(1, 2 ** len(buttons)):
            split_bin = [int(s) for s in bin(i)[2:].zfill(len(buttons))]

            toggles = [buttons[b_i] for b_i, to_press in enumerate(split_bin) if to_press == 1]

            state = 0
            for i in toggles:
                state ^= i

            if state == indicator:
                press_ct = sum(split_bin)
                best = min(best, press_ct)
                if verbose:
                    print(f'\tValid: {split_bin} = {press_ct} press{"es" if press_ct > 1 else ""}')

        if verbose:
            print(f'Best: {best} press{"es" if best > 1 else ""}')

        acc += best

    return acc


def p2():
    acc = 0
    for line in data:
        sp = line.split()

        joltages = get_ints(sp[-1])
        j_len = len(joltages)

        buttons_raw = [set(get_ints(s)) for s in sp[1:-1]]
        buttons = [[1 if i in b_set else 0 for i in range(j_len)] for b_set in buttons_raw]
        b_len = len(buttons)

        multipliers = [z3.Int(f'm{i}') for i in range(len(buttons))]

        if verbose:
            print(f'\nTarget vector: {joltages}\nButton vectors: {buttons}')

        opt = z3.Optimize()

        for mult in multipliers:
            opt.add(mult >= 0)

        for j_i in range(j_len):
            opt.add(z3.Sum([multipliers[b_i] for b_i in range(b_len) if (buttons[b_i][j_i]) == 1]) == joltages[j_i])

        total = z3.Sum(multipliers)

        if verbose:
            print('Constraints:')
            for s in opt.assertions():
                print(f'\t{s}')

        opt.minimize(total)
        result = opt.check()

        if verbose:
            print(f'{result}')

        model = opt.model()

        result_vector = [model[multiplier].as_long() for multiplier in multipliers]
        presses = sum(result_vector)

        if verbose:
            print(f'Best multiplier vector: {result_vector} = {presses}')

        acc += presses

    return acc


if __name__ == '__main__':
    setday(10)

    data = parselines()

    print('part1:', p1())
    print('part2:', p2())
