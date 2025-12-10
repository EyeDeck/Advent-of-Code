from aoc import *

import z3


def p1():

    @memo
    def get_bit_order(n):
        x = [i for i in range(1, 2 ** n)]
        x.sort(key=int.bit_count)
        return x

    acc = 0
    for line in data:
        sp = line.split()
        indicator = sum((1 if s == '#' else 0) << i for i, s in enumerate(sp[0].strip('[]')))
        buttons = [sum(1 << i for i in get_ints(s)) for s in sp[1:-1]]
        b_len = len(buttons)

        if verbose:
            print(f'\nTarget: {bin(indicator)}\nXOR values: {[bin(i) for i in buttons]}')

        best = 0
        for button_bitmask in get_bit_order(b_len):
            state = 0
            for i in range(b_len+1):
                if (1 << i) & button_bitmask:
                    state ^= buttons[i]

            if state == indicator:
                best = button_bitmask.bit_count()
                if verbose:
                    print(f'Best: {button_bitmask} = {best} press{"es" if best > 1 else ""}')
                break

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
