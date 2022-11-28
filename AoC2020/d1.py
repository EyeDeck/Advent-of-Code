inp = [int(l) for l in open('d1.txt').readlines()]

def p1():
    for i in inp:
        for j in inp:
            if j+i == 2020:
                return i*j
def p2():
    for i in inp:
        for j in inp:
            for k in inp:
                if j+i+k == 2020:
                    return j*i*k

print(f'part1: {p1()}')
print(f'part2: {p2()}')
