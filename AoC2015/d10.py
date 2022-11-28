import sys


def step(num):
    out = []
    buffer_n = num[0]
    buffer_ct = 1
    for n in num[1:]:
        if n == buffer_n:
            buffer_ct += 1
        else:
            out.extend([str(buffer_ct), buffer_n])
            buffer_n = n
            buffer_ct = 1
    out.extend([str(buffer_ct), buffer_n])
    return ''.join(out)


def step_n(num, ct):
    for i in range(ct):
        num = step(num)
    return num


day = 10
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().strip()

print(f'part1: {len(step_n(data, 40))}')
print(f'part2: {len(step_n(data, 50))}')
