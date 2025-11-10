from ec import *


def cadd(a,b):
    X1, X2 = a
    Y1, Y2 = b
    return vadd(a,b)


def cmul(a,b):
    X1, Y1 = a
    X2, Y2 = b
    return [X1 * X2 - Y1 * Y2, X1 * Y2 + Y1 * X2]


def cdiv(a,b):
    return tuple(int(f) for f in vdiv(a,b))


def p1():
    A = parse_lines(1, get_ints)[0]
    R = [0,0]
    for _ in range(3):
        R = cmul(R,R)
        R = cdiv(R, [10,10])
        R = cadd(R, A)
    return str(list(R)).replace(' ', '')


def p2():
    A = parse_lines(2, get_ints)[0]

    acc = 0
    grid = {}
    for y in range(101):
        for x in range(101):
            point = vadd(A,(x*10,y*10))

            R = [0,0]
            for i in range(100):
                R = cmul(R,R)
                R = cdiv(R, (100000,100000))
                R = cadd(R, point)
                if R[0] > 1000000 or R[0] < -1000000 or R[1] > 1000000 or R[1] < -1000000:
                    break
            else:
                # print(point, R)
                acc += 1
                grid[x,y] = 'x'

    # print(grid)
    print_2d('. ', grid)
    return acc


def p3():
    A = parse_lines(3, get_ints)[0]

    acc = 0
    grid = {}
    for y in range(1001):
        for x in range(1001):
            point = vadd(A, (x,y)) # (x*10,y*10))

            R = [0,0]
            for i in range(100):
                R = cmul(R,R)
                R = cdiv(R, (100000,100000))
                R = cadd(R, point)
                if R[0] > 1000000 or R[0] < -1000000 or R[1] > 1000000 or R[1] < -1000000:
                    break
            else:
                # print(point, R)
                acc += 1
                grid[x,y] = 'x'

    # print(grid)
    # print_2d('. ', grid)
    return acc


setquest(2)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
