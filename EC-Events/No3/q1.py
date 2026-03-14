from ec import *


def p1():
    data = parse_lines(1)
    acc = 0
    for line in data:
        identifier, colors = line.split(':')
        r,g,b = [int(''.join('0' if c.islower() else '1' for c in x), 2) for x in colors.split()]
        if g > r and g > b:
            acc += int(identifier)
    return acc


def p2():
    data = parse_lines(2)
    shiny_bins = defaultdict(dict)
    for line in data:
        identifier, colors = line.split(':')
        r,g,b,s = [int(''.join('0' if c.islower() else '1' for c in x), 2) for x in colors.split()]
        shiny_bins[s][r+b+g] = int(identifier)
    shiniest_bin = shiny_bins[max(shiny_bins)]
    return shiniest_bin[min(shiniest_bin)]


def p3():
    data = parse_lines(3)
    shiny_bins = defaultdict(list)
    for line in data:
        identifier, colors = line.split(':')
        r,g,b,s = [int(''.join('0' if c.islower() else '1' for c in x), 2) for x in colors.split()]
        if s <= 30:
            shininess = 'matte'
        elif s >= 33:
            shininess = 'shiny'

        if r > g and r > b:
            color = 'red'
        elif g > r and g > b:
            color = 'green'
        elif b > r and b > g:
            color = 'blue'

        shiny_bins[f'{color}-{shininess}'].append(int(identifier))

    print(shiny_bins)
    return sum(max(shiny_bins.values(), key=len))


setquest(1)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
