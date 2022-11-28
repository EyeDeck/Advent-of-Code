import sys


def p2(d):
    d = set(d)
    for seat in d:
        if seat+1 not in d and seat+2 in d:
            return seat+1


# alternate formula
def p2_alt(d):
    return ((d[-1]-d[0]+1) * (d[0]+d[-1]) // 2) - sum(d)


f = 'd5.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = sorted([int(line.translate(str.maketrans('BFRL', '1010')), 2) for line in file.readlines()])

print(f'part1: {data[-1]}')  # or max(data)
print(f'part2: {p2(data)}')
print(f'part2 (alt algo): {p2_alt(data)}')

# cheeky one-liner:
# print(max(d:=sorted(int(l.translate({66:49,70:48,76:48,82:49}),2)for l in open('d5.txt'))),((d[-1]-d[0]+1)*(d[0]+d[-1])//2)-sum(d))

# import time
# start = time.process_time()
# for i in range(100000):
#     p2(data)
# print(f'p2*10k took {time.process_time() - start}')
#
# start = time.process_time()
# for i in range(100000):
#     p2_alt(data)
# print(f'p2_alt*10k took {time.process_time() - start}')
