import sys


def p1():
    for i in range(25, len(data)):
        sums = set()
        nt = data[i]
        ct = 0
        for j in range(i - 25, i):
            for k in range(i - 25, i):
                sums.add(data[j] + data[k])
                ct += 1
        # print('ct', ct)

        # print(sums)
        if nt not in sums:
            return nt
        # break

    return None


# I'm pretty sure there are some off-by-ones in here but it works anyway so fuck it
def p2():
    for length in range(2, len(data)):
        # print(length)
        for i in range(len(data) - length):
            total = sum(data[i:i + length])
            if total == weakness:
                # print(f'sum of {data[i:i+length]} is {weakness}')
                return min(data[i:i + length]) + max(data[i:i + length])
        else:
            print(data[i:i + length])


f = 'd9.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [int(line) for line in file]

weakness = p1()

print(f'part1: {weakness}')
print(f'part2: {p2()}')
