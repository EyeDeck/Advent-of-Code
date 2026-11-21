from ec import *

seggos = {
    '0': 6,
    '1': 2,
    '2': 5,
    '3': 5,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 3,
    '8': 7,
    '9': 6,
    '+': 2,
    '-': 1,
    '=': 2,
    ' ': 0,
    'A': 6,
}

seggo_gain = {
    '0': ['8'],
    '1': ['7'],
    '2': [],
    '3': ['9'],
    '4': [],
    '5': ['9', '6'],
    '6': ['8'],
    '7': [],
    '8': [],
    '9': ['8'],
    'A': ['8'],
    '+': [],
    '-': ['+'],
    '=': [],
    ' ': [],
}

seggo_lose = {
    '0': [],
    '1': [],
    '2': [],
    '3': [],
    '4': [],
    '5': [],
    '6': ['5'],
    '7': ['1'],
    '8': ['0', '6', '9', 'A'],
    '9': ['3', '5'],
    'A': [],
    '+': ['-'],
    '-': [],
    '=': [],
    ' ': [],
}

seggo_shift = {
    '0': ['6', '9', 'A'],
    '1': [],
    '2': ['3'],
    '3': ['2', '5'],
    # '4': ['11'],  #?
    '4': [],
    '5': ['3'],
    '6': ['0', '9', 'A'],
    '7': [],
    '8': [],
    '9': ['0', '6', 'A'],
    'A': ['0', '6', '9'],
    '+': [],
    '-': [],
    '=': [],
    ' ': [],
}


def p1():
    data = parse_lines(1)

    acc = 0
    for line in data:
        segs = sum(seggos[c] for c in line)

        if eval(line.replace('=', '==')):
            acc += segs

    return acc


def p2():
    data = parse_lines(2)

    acc = 0
    for line in data:
        segs = sum(seggos[c] for c in line)

        if eval(fix_for_eval(line)):
            acc += segs

    return base_repr(acc, base=11)


def fix_for_eval(s):
    s = s.replace(' ', '')
    s = s.replace('=', ' == ')
    s = s.replace('+', ' + ')
    s = s.replace('-', ' - ')
    s = ' '.join((f'int("{x}", 11)' if x not in ['-', '+', '=='] else x) for x in s.split(' '))
    return s


def check_self_swap(s):
    for i in range(len(s)):
        c = s[i]
        for swap in seggo_shift[c]:
            new_s = s[:i] + swap + s[i + 1:]
            new_s = fix_for_eval(new_s)
            if eval(new_s):
                return True
    return False


def check_distant_swap(s):
    for i in range(len(s)):
        c_a = s[i]

        for swap_a in seggo_lose[c_a]:
            new_s = s[:i] + swap_a + s[i + 1:]

            for j in range(len(s)):
                if i == j:
                    continue

                c_b = new_s[j]

                for swap_b in seggo_gain[c_b]:
                    newer_s = new_s[:j] + swap_b + new_s[j + 1:]

                    newer_s = fix_for_eval(newer_s)

                    if eval(newer_s):
                        return True
    return False


def p3():
    data = parse_lines(3)

    acc = 0
    for line in data:
        segs = sum(seggos[c] for c in line)

        if eval(fix_for_eval(line)):
            acc += segs
        elif check_self_swap(line):
            acc += segs
        elif check_distant_swap(line):
            acc += segs

    return base_repr(acc, base=11)


if __name__ == '__main__':
    setquest(20)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
