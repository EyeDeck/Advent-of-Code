import hashlib
from aoc import *


def solve(inp, p2 = False):
    cmp = "0" * 5
    password = [c for c in "_" * 8]
    print("".join(password), end="\r")
    i = 0
    n = 0
    while n < 8:
        md5 = hashlib.new("md5")
        md5.update(str.encode(inp + str(i)))
        h = md5.hexdigest()
        if h[:5] == cmp:
            if p2:
                if h[5] in "01234567" and password[int(h[5])] == '_':
                    password[int(h[5])] = h[6]
                    n += 1
            else:
                password[n] = h[5]
                n += 1
            print("".join(password), end="\r")
        i += 1
    return "".join(password)


def p2():
    return None


day = 5
if len(sys.argv) > 1:
    data = sys.argv[1]
else:
    data = 'cxdnnyjw'

print(f'part1: {solve(data)}')
print(f'part2: {solve(data, True)}')
