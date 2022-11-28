import sys


def p1():
    strings = []
    for line in data:
        line = line[1:-1]
        s = ""
        i = 0
        while i < len(line):
            c = line[i]
            if c == '\\':
                n = line[i+1]
                if n == 'x':
                    s += chr(int(line[i+2:i+4], 16))
                    i += 3
                else:
                    s += n
                    i += 1
            else:
                s += c
            i += 1
        # print(f'{line} ->\n{s}')
        strings.append(s)
    return sum([len(data[i]) - len(strings[i]) for i in range(len(data))])


def p2():
    strings = []
    for line in data:
        s = ""
        i = 0
        while i < len(line):
            c = line[i]
            if c == '\\':
                s += '\\\\'
            elif c == '"':
                s += '\\\"'
            else:
                s += c
            i += 1
        s = '"' + s + '"'
        # print(f'{line} ->\n{s}\n')
        strings.append(s)

    return sum([len(strings[i]) - len(data[i]) for i in range(len(data))])


day = 8
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
