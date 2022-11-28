import sys


def inc(s):
    o = -1
    while True:
        if s[o] == 'z':
            s[o] = 'a'
            o -= 1
        else:
            s[o] = chr(ord(s[o]) + 1)
            if s[o] in 'iol':
                if s[o] == 'i':
                    s[o] = 'j'
                elif s[o] == 'o':
                    s[o] = 'p'
                else:
                    s[o] = 'm'
            return s
        if o < -len(s):
            return s


def not_banned(s):
    return 'i' not in s and 'o' not in s and 'l' not in s


def has_increasing(s):
    for i, c in enumerate(s[:-2]):
        if s[i+1] == chr(ord(c)+1) and s[i+2] == chr(ord(c)+2):
            # print(s[i], s[i+1], s[i+2])
            return True
    return False


def count_pairs(s):
    ct = 0
    seen = []
    for i, c in enumerate(s[:-1]):
        if c not in seen and s[i+1] == c:
            seen.append(c)
            ct += 1
    return ct


def get_next(pw):
    pw = [c for c in pw]
    while True:
        if not_banned(pw) and has_increasing(pw) and count_pairs(pw) >= 2:
            return ''.join(pw)
        pw = inc(pw)


def p2():
    return None


day = 11
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().strip()

p1 = get_next(data)
p2 = get_next(inc([c for c in p1]))
print('part1: %s\npart2: %s' % (p1, p2))
