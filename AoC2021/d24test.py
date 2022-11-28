import sys

inp = list(reversed([int(i) for i in sys.argv[1:]]))

w, x, y, z = 0, 0, 0, 0


def mult(w, a, b, z):
    x = 0 if ((z % 26) + a) == w else 1
    # print(x)
    z = z * ((25 * x) + 1) + ((w + b) * x)
    # print(w, y, x, z)
    return z


def div(w, a, b, z):
    x = 0 if ((z % 26) + a) == w else 1
    # print(x)
    z //= 26
    z = z * ((25 * x) + 1) + (x * (w + b))
    # print(w, y, x, z)
    return z


z = 0
z = mult(inp.pop(), 12, 7, z)
z = mult(inp.pop(), 11, 15, z)
z = mult(inp.pop(), 12, 2, z)
z = div(inp.pop(), 3, 15, z)
z = mult(inp.pop(), 10, 14, z)
z = div(inp.pop(), -9, 2, z)
z = mult(inp.pop(), 10, 15, z)
z = div(inp.pop(), -7, 1, z)
z = div(inp.pop(), -11, 15, z)
z = div(inp.pop(), -4, 15, z)
z = mult(inp.pop(), 14, 12, z)
z = mult(inp.pop(), 11, 2, z)
z = div(inp.pop(), -8, 13, z)
z = div(inp.pop(), -10, 13, z)

print(z)