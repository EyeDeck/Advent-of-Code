from aoc import *


def p1():
    block_map = []
    state = True
    id = 0
    for char in data:
        i = int(char)
        if state:
            for _ in range(i):
                block_map.append(id)
            id += 1
        else:
            for _ in range(i):
                block_map.append(None)
        state = not state

    l = 0
    while True:
        try:
            while block_map[l] is not None:
                l += 1
        except IndexError:
            break

        block = block_map.pop()
        if block is None:
            continue
        block_map[l] = block

    return sum(i * n for i, n in enumerate(block_map))


def p2():
    meta_filled = {}

    free_bins = defaultdict(list)
    state = True
    id = 0
    pos = 0
    for char in data:
        i = int(char)
        if state:
            meta_filled[id] = (pos, i)
            pos += i
        else:
            if i != 0:
                free_bins[i].append(pos)
            pos += i
            id += 1
        state = not state

    for bin in free_bins.values():
        heapq.heapify(bin)

    for id, (position, length) in reversed(meta_filled.items()):

        lowest_in_best_bin = INF
        best_bin = -1
        for bin_length, current_bin in free_bins.items():
            if bin_length < length:
                continue
            lowest_in_bin = current_bin[0]
            if lowest_in_bin < lowest_in_best_bin:
                best_bin = bin_length
                lowest_in_best_bin = lowest_in_bin

        if lowest_in_best_bin == INF or lowest_in_best_bin > position:
            continue

        heapq.heappop(free_bins[best_bin])

        if len(free_bins[best_bin]) == 0:
            del free_bins[best_bin]
        meta_filled[id] = (lowest_in_best_bin, length)

        leftover = best_bin - length
        if leftover > 0:
            heapq.heappush(free_bins[leftover], lowest_in_best_bin + length)

    acc = 0
    for k, v in meta_filled.items():
        for n in range(v[0], v[0] + v[1]):
            acc += n * k
    return acc


setday(9)

data = parselines()[0]

print('part1:', p1())
print('part2:', p2())
