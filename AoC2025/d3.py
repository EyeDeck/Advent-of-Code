from aoc import *


def solve(n):
    s_range = [str(i) for i in range(9,0,-1)]
    acc = 0
    for line in data:
        found = []
        current_index = 0
        for limit in range(n, 0, -1):
            l, r = current_index, len(line) - limit + 1
            for s in s_range:
                pos = line.find(s, l, r)
                if pos >= 0:
                    s = line[pos]
                    found.append(s)
                    current_index = pos + 1
                    break
        best = int(''.join(found))
        acc += best
    return acc



# def solve(n):
#     digits = {str(i) for i in range(9,0,-1)}
#
#     acc = 0
#     for line in data:
#         print(line)
#         found = []
#         search_positions = {k:-1 for k in digits}
#         search_index = 0
#         current_index = 0
#         for limit in range(n, 0, -1):
#             l, r = current_index, len(line) - limit + 1
#             unfound = digits.copy()
#
#             while search_positions['9'] < current_index and search_index <= r and unfound:
#                 c = line[search_index]
#                 if c in unfound:
#                     search_positions[c] = search_index
#                     unfound.remove(c)
#                 search_index += 1
#                 print(search_positions, search_index)
#             print(search_positions.items())
#
#             c, pos = max((x for x in search_positions.items() if x[1] > current_index), key=lambda x:x[0])
#
#             found.append(c)
#             search_index = current_index
#             print('\t', found, search_index)
#
#         best = int(''.join(found))
#         acc += best
#     return acc


if __name__ == '__main__':
    setday(3)

    data = parselines()

    print('part1:', solve(2))
    print('part2:', solve(12))
