from aoc import *

def p1():
    lowest = INF
    for seed in seeds:
        curr_val = seed
        for key in key_order:
            ranges = maps[key]
            for r in ranges:
                if r[1] <= curr_val <= (r[1] + r[2]):
                    curr_val = r[0] - r[1] + curr_val
                    break
        lowest = min(lowest, curr_val)
    return lowest


def p2():
    it = iter(seeds)
    unsolved_ranges = []
    for seed in it:
        seed_range = next(it)
        unsolved_ranges.append((seed, seed + seed_range - 1))

    for key in key_order:
        ranges = maps[key]
        next_unsolved = []
        for r in ranges:
            r_low = r[1]
            r_high = r[1] + r[2] - 1
            offset = r[0] - r[1]
            work = True
            while work:
                work = False
                to_pop = []
                to_reprocess = []
                for ur in unsolved_ranges:
                    ur_low = ur[0]
                    ur_high = ur[1]
                    if (r_low <= ur_low <= r_high) or (r_low <= ur_high <= r_high):
                        work = True
                        to_pop.append(ur)
                        if (r_low <= ur[0]) and (r_high >= ur[1]):
                            # range fits entirely within mapping
                            next_unsolved.append((ur_low+offset, ur_high+offset))
                        elif r_low <= ur_low:
                            # left part of range overlaps mapping, so split
                            next_unsolved.append((ur_low+offset, r_high+offset))
                            to_reprocess.append((r_high+1, ur_high))
                        else:
                            # right part of range overlaps mapping, so split
                            to_reprocess.append((ur_low, r_low-1))
                            next_unsolved.append((r_low+offset, ur_high+offset))

                for p in to_pop:
                    unsolved_ranges.remove(p)

                for p in to_reprocess:
                    unsolved_ranges.append(p)
        unsolved_ranges += next_unsolved

    return min(unsolved_ranges)[0]

setday(5)

with open_default() as file:
    data = [block for block in file.read().strip().split('\n\n')]
    seeds = [int(i) for i in data[0].split(':')[1].strip().split()]
    maps = defaultdict(list)
    for block in data[1:]:
        block = block.split('\n')
        map_name = block[0].split()[0]
        for line in block[1:]:
            line = [int(i) for i in line.split()]
            maps[map_name].append(line)
    # print(seeds, maps)
    key_order = maps.keys()

print('part1:', p1() )
print('part2:', p2() )
