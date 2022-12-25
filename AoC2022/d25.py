import sys

decode_map = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}


def decode(s):
    n = 0
    for i, c in enumerate(reversed(s)):
        n += decode_map[c] * (5 ** i)
    return n


encode_map = {
    0: ('0', 0),
    1: ('1', -1),
    2: ('2', -2),
    3: ('=', 2),  # really only these two positive ones need defining
    4: ('-', 1)
}


def encode(n):
    snafu = []
    while n > 0:
        d = (n % 5)
        a, acc_mod = encode_map[d]
        n += acc_mod
        snafu.append(a)
        n //= 5
    return ''.join(reversed(snafu))


def p1():
    acc = 0
    for line in data:
        acc += decode(line)
    print(acc)
    return encode(acc)


day = 25
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

print('part1:', p1())
