# oh my god I went full retard today please don't look here
inp = [int(i) for i in open('d4-bb.txt').read().split('-')]

p1 = 0
p2 = 0
i = inp[0]
while i < inp[1]:
    digits = [i for i in str(i)]
    m = len(digits) - 1
    valid = True

    # ascending or equal
    for j in range(0, m):
        if int(digits[j]) > int(digits[j + 1]):
            digits[j + 1] = digits[j]  # hasty but obvious massive optimization
            i = int(''.join(digits))
            valid = False
            break
    if not valid:
        continue

    # has a dub
    valid = False
    for j in range(0, m):
        if digits[j] == digits[j + 1]:
            valid = True
            break
    if not valid:
        i += 1
        continue

    p1 += 1
    valid = False
    # blacklist the trips
    trips = set()
    for j in range(0, m-1):
        if digits[j] == digits[j + 1] and digits[j] == digits[j + 2]:
            trips.add(digits[j])
    # find non blacklisted dubs
    for j in range(0, m):
        if digits[j] == digits[j + 1] and digits[j] not in trips:
            valid = True
            break

    if valid:
        p2 += 1
    i += 1

print('p1: {}\np2: {}'.format(p1, p2))
