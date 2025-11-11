from ec import *


def cadd(a,b):
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


def p2(p3=False):
    A = parse_lines(3 if p3 else 2, get_ints)[0]

    acc = 0
    grid = {}
    grid_size, point_mult = (1001, 1) if p3 else (101, 10)
    for y in range(grid_size):
        for x in range(grid_size):
            point = vadd(A,(x*point_mult,y*point_mult))

            R = [0,0]
            for i in range(100):
                R = cmul(R,R)
                R = cdiv(R, (100000,100000))
                R = cadd(R, point)

                # if any(not (-1000000 <= i <= 1000000) for i in R):  # wew lad that's slow
                if not (-1000000 <= R[0] <= 1000000) or not (-1000000 <= R[1] <= 1000000):
                    break
            else:
                acc += 1
                if verbose:
                    grid[x,y] = 'x'

    if verbose:
        print_2d('. ', grid)
    return acc


setquest(2)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2(False))
print('part3:', p2(True))
