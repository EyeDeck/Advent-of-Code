from aoc import *


def p1():
    blockmap = []
    state = True
    id = 0
    for char in data:
        i = int(char)
        if state:
            for _ in range(i):
                blockmap.append(id)
            id += 1
        else:
            for _ in range(i):
                blockmap.append(None)
        state = not state
    # print(blockmap)
    l = 0
    while True:
        try:
            while blockmap[l] != None:
                l += 1
        except IndexError:
            break
        # print(l, len(blockmap))
        block = blockmap.pop()
        if block == None:
            continue
        blockmap[l] = block
    # print(blockmap)
    return sum(i * n for i, n in enumerate(blockmap))


def p2():
    meta_filled = {}
    # meta_free = {}
    free_bins = defaultdict(set)
    state = True
    id = 0
    pos = 0
    for char in data:
        i = int(char)
        if state:
            meta_filled[id] = (pos, i)
            pos += i
            # for _ in range(i):
            #     map.append(id)
        else:
            # meta_free[id] = [len(map), i]
            if i != 0:
                free_bins[i].add(pos)
            pos += i
            # for _ in range(i):
            #     map.append(None)
            id += 1
        state = not state

    # print(meta_filled)
    # print(free_bins)

    def get_best_bin(bins):
        lowest = INF
        best_bin = -1
        for bin in bins:
            lowest_in_bin = min(free_bins[bin])
            if lowest_in_bin < lowest:
                best_bin = bin
                lowest = lowest_in_bin
        return best_bin, lowest

    for id, (position, length) in reversed(meta_filled.items()):
        compatible_bins = [k for k in free_bins.keys() if k >= length]
        best_bin, lowest_in_best_bin = get_best_bin(compatible_bins)
        if lowest_in_best_bin == INF or lowest_in_best_bin > position:
            continue
        leftover = best_bin - length
        free_bins[best_bin].remove(lowest_in_best_bin)
        if len(free_bins[best_bin]) == 0:
            # print('deleted bin', best_bin)
            del free_bins[best_bin]
        meta_filled[id] = (lowest_in_best_bin, length)
        # print(f'id {id} position {position} length {length} leftover {leftover} moved to {lowest_in_best_bin}')
        if leftover > 0:
            free_bins[leftover].add(lowest_in_best_bin + length)
            # print(f'added leftover {leftover} at pos {lowest_in_best_bin + length}')

    # print(meta_filled)
    # print(free_bins)
    acc = 0
    for k, v in meta_filled.items():
        for n in range(v[0], v[0] + v[1]):
            acc += n * k
    return acc


setday(9)

data = parselines()[0]

print('part1:', p1())
print('part2:', p2())
