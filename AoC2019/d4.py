import sys
f = 'd4.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]
inp = open(f).read().split('-')


def get_next_ascending(num):
    s = str(num)
    ln = len(s)
    ints = [int(i) for i in s]
    for i in range(0, ln-1):
        if ints[i] > ints[i+1]:
            return int(''.join(s[:i] + s[i]*(ln-i)))
    return num


def check_em(num, digit, ct):
    if digit * ct in num:
        return True
    return False


p1, p2 = 0, 0
i, end = int(inp[0]), int(inp[1])
while True:
    i = get_next_ascending(i)
    if i > end:
        break

    i_str = str(i)
    digit_set = set(i_str)

    dubs = False
    for d in digit_set:
        if check_em(i_str, d, 2):
            dubs = True
            if not check_em(i_str, d, 3):
                p2 += 1
                break
    if dubs:
        p1 += 1

    i += 1

print('p1: {}\np2: {}'.format(p1, p2))
