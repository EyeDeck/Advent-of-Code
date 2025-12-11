from aoc import *


@memo
def count_paths(src, tgt):
    if src == tgt:
        return 1
    count = 0
    if src in data:
        for v in data[src]:
            count += count_paths(v, tgt)
    return count


if __name__ == '__main__':
    setday(11)

    data = {line[0][:-1]: line[1:] for line in parselines(str.split)}

    print('part1:', count_paths('you', 'out'))
    print('part2:', count_paths('svr', 'fft') * count_paths('fft', 'dac') * count_paths('dac', 'out'))
