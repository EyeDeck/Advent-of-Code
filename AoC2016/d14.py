import hashlib
from aoc import *

def solve(stretch):
    three = re.compile(r'(.)\1{2}')
    five = re.compile(r'(.)\1{4}')

    finds = defaultdict(list)
    asdf = {}

    passwords = []
    i = 0
    final = 1_000_000
    while i < final:

        hash = (data + str(i))
        for _ in range(stretch+1):
            md5 = hashlib.md5()
            md5.update(hash.encode())
            hash = md5.hexdigest()

        five_result = five.search(hash)
        if five_result:
            s = five_result.group()
            s_3 = s[:3]
            finds[s_3] = [n for n in finds[s_3] if (n + 1000) > i]

            print(hash, s, i, s_3, finds[s_3])

            passwords += finds[s_3]
            finds[s_3].clear()

            if len(passwords) >= 64:
                final = i + 1000

        three_result = three.search(hash)
        if three_result:
            s = three_result.group()
            finds[s].append(i)
            asdf[i] = hash
            # print('cached', s, i)

        i += 1

    passwords.sort()
    # print(passwords)
    return passwords[63]


setday(14)

data = parselines()[0]
# data = 'abc'

print('part1:', solve(0) )
print('part2:', solve(2016) )
