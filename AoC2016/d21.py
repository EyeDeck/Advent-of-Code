from aoc import *


def scramble_word(start):
    scramble = [c for c in start]
    for line in data:
        ins = line.split()
        a,b,c = ins[0:3]
        z = ins[-1]
        if a == 'swap':
            if b == 'position':
                x, y = int(c), int(z)
            elif b == 'letter':
                x, y = scramble.index(c), scramble.index(z)
            scramble[x], scramble[y] = scramble[y], scramble[x]
        elif a == 'rotate':
            if b == 'based':
                n = scramble.index(z)
                if n >= 4:
                    n += 1
                n += 1
                n %= len(start)
                scramble = scramble[-n:] + scramble[:-n]
            else:
                n = int(c)
                if b == 'left':
                    scramble = scramble[n:] + scramble[:n]
                elif b == 'right':
                    scramble = scramble[-n:] + scramble[:-n]

        elif a == 'reverse':
            x, y = int(c), int(z)
            scramble = scramble[:x] + [*reversed(scramble[x:y+1])] + scramble[y+1:]
        elif a == 'move':
            x, y = int(c), int(z)
            scramble.insert(y, scramble.pop(x))

        # print(f'{line} = {"".join(scramble)}')
    return ''.join(scramble)


def unscramble_word(start):
    rev_map = {1:0, 3:1, 5:2, 7:3, 2:4, 4:5, 6:6, 0:7}
    rev_map = {k:v-k for k,v in rev_map.items()}

    scramble = [c for c in start]
    for line in data[::-1]:
        ins = line.split()
        a,b,c = ins[0:3]
        z = ins[-1]
        if a == 'swap':
            if b == 'position':
                x, y = int(c), int(z)
            elif b == 'letter':
                x, y = scramble.index(c), scramble.index(z)
            scramble[x], scramble[y] = scramble[y], scramble[x]
        elif a == 'rotate':
            if b == 'based':
                n = rev_map[scramble.index(z)]
                scramble = scramble[-n:] + scramble[:-n]
            else:
                n = int(c)
                if b == 'left':
                    scramble = scramble[-n:] + scramble[:-n]
                elif b == 'right':
                    scramble = scramble[n:] + scramble[:n]
        elif a == 'reverse':
            x, y = int(c), int(z)
            scramble = scramble[:x] + [*reversed(scramble[x:y+1])] + scramble[y+1:]
        elif a == 'move':
            x, y = int(c), int(z)
            scramble.insert(x, scramble.pop(y))

        # print(f'{line} = {"".join(scramble)}')
    answer = ''.join(scramble)
    # print(answer, scramble_word(answer))
    assert start == scramble_word(answer)

    return answer


setday(21)

data = parselines()

print('part1:', scramble_word('abcdefgh') )
print('part2:', unscramble_word('fbgdceah') )
