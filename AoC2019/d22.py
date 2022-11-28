import re
import sys
from collections import deque


def dns_deck(stack):
    stack.reverse()
    return stack


def cut_deck(stack, ct):
    stack.rotate(-ct)
    return stack


def dwi_deck(stack, inc):
    stack_len = len(stack)
    new_stack = [0 for _ in range(stack_len)]
    j = 0
    for i in range(stack_len):
        new_stack[j] = stack[i]
        j += inc
        j %= stack_len
    return deque(new_stack)


f = 'd22.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [line.split() for line in  open(f).readlines()]
parsed = []
for line in inp:
    if line[0] == 'cut':
        parsed.append([cut_deck, int(line[-1])])
    elif line[1] == 'with':
        parsed.append([dwi_deck, int(line[-1])])
    elif line[1] == 'into':
        parsed.append([dns_deck])

deck = deque([i for i in range(10007)])
for ins in parsed:
    args = [deck]
    if len(ins) > 1:
        args.append(*ins[1:])
    # print(args)
    deck = ins[0](*args)
print(f'p1 {deck.index(2019)}')


# I had almost zero chance of working this out on my own, so I stole the following bits
# fuck you, Eric

def solve(c, n, p, o=0, i=1):
    inv = lambda x: pow(x, c-2, c)
    for s in [s.split() for s in open('input.txt').readlines()]:
        if s[0] == 'cut':  o += i * int(s[-1])
        if s[1] == 'with': i *= inv(int(s[-1]))
        if s[1] == 'into': o -= i; i *= -1
    o *= inv(1-i); i = pow(i, n, c)
    return (p*i + (1-i)*o) % c

def do_the_thing_I_do_not_understand(c, n, p, o=0, i=1):
    o *= inv(1 - i)
    i = pow(i, n, c)
    return (p * i + (1 - i) * o) % c


def inv(n, mod):
    return pow(n, mod - 2, mod)

cards = 119315717514047
repeats = 101741582076661
o = 0
i = 1
for ins in parsed:
    if ins[0] == dns_deck:
        o -= i
        i *= -1
    elif ins[0] == cut_deck:
        o += i * ins[1]
    elif ins[0] == dwi_deck:
        i *= inv(ins[1], cards)
o *= inv(1 - i, cards)
i = pow(i, repeats, cards)
print((2020*i + (1-i)*o) % cards)

# print((pow(A, n, D)*X + (pow(A, n, D)-1) * modinv(A-1, D) * B) % D)
