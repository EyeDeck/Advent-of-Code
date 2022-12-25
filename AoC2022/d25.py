import sys

decode_map = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}

encode_map = {
    0: ('0', 0),
    1: ('1', -1),
    2: ('2', -2),
    3: ('=', 2),  # really only these two positive ones need defining
    4: ('-', 1)
}


def p1():
    acc = 0
    for line in data:
        n = 0
        for i, c in enumerate(reversed(line)):
            n += decode_map[c] * (5 ** i)
        acc += n

    snafu = []
    while acc > 0:
        d = (acc % 5)
        # print(acc, snafu, d)

        a, acc_mod = encode_map[d]

        acc += acc_mod
        snafu.append(a)

        acc //= 5

    return ''.join(reversed(snafu))


day = 25
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

print('part1:', p1())
