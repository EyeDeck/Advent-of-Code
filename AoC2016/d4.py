import sys
from collections import Counter


def solve():
    count = 0
    real = []
    for k, v in data.items():
        ct = Counter(sorted(k))
        del ct['-']
        checksum = ''.join([x[0] for x in ct.most_common(5)])
        if checksum == v[1]:
            count += v[0]
            real.append((k,v[0]))
    print(f'part1: {count}')
    decrypted = {''.join(chr(((ord(c)-97 + x[1]) % 26)+97) if c != '-' else ' ' for c in x[0]): x[1] for x in real}
    print(f'part2: {decrypted["northpole object storage"]}')


day = 4
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = {(x := line.strip().split('['))[0][:-4]: [int(x[0][-3:]), x[1].strip(']')] for line in file}

solve()
