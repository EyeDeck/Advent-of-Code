from aoc import *

def p1():
    seeds = [int(i) for i in data[0].split(':')[1].strip().split()]
    # print(seeds)
    maps = defaultdict(list)
    for block in data[1:]:
        block = block.split('\n')
        map_name = block[0].split()[0]
        for line in block[1:]:
            line = [int(i) for i in line.split()]
            maps[map_name].append(line)
    # print(seeds, maps)
    key_order = maps.keys()
    lowest = INF
    for seed in seeds:
        # print(seed)
        curr_val = seed
        for key in key_order:
            ranges = maps[key]
            # print(ranges)
            for r in ranges:
                if r[1] <= curr_val <= (r[1] + r[2]):
                    # print('in range', r)
                    offset = r[0] - r[1]
                    # print('offset', offset)
                    curr_val = r[0] - r[1] + curr_val
                    # print('next = ', curr_val)
                    break
        lowest = min(lowest, curr_val)
    return lowest


def p2_bruteforce():
    seeds = [int(i) for i in data[0].split(':')[1].strip().split()]
    # print(seeds)
    maps = defaultdict(list)
    for block in data[1:]:
        block = block.split('\n')
        map_name = block[0].split()[0]
        for line in block[1:]:
            line = [int(i) for i in line.split()]
            maps[map_name].append(line)
    # print(seeds, maps)
    key_order = maps.keys()
    lowest = INF
    it = iter(seeds)
    for seed_start in it:
        print('seed_start', seed_start)
        seed_range = next(it)
        for seed in range(seed_start, seed_start + seed_range):
            curr_val = seed
            for key in key_order:
                # print(key, curr_val)
                ranges = maps[key]
                # print(ranges)
                for r in ranges:
                    if r[1] <= curr_val < (r[1] + r[2]):
                        curr_val = r[0] - r[1] + curr_val
                        # print('  ', curr_val)
                        break
            # print('  ', curr_val)
            lowest = min(lowest, curr_val)
    return lowest

def p2():
    seeds = [int(i) for i in data[0].split(':')[1].strip().split()]
    # print(seeds)
    maps = defaultdict(list)
    for block in data[1:]:
        block = block.split('\n')
        map_name = block[0].split()[0]
        for line in block[1:]:
            line = [int(i) for i in line.split()]
            maps[map_name].append(line)
    print(seeds, maps)
    key_order = maps.keys()
    lowest = INF

    it = iter(seeds)
    for seed in it:
        print('\n\nseed', seed)
        seed_range = next(it)
        unsolved_ranges = [(seed, seed+seed_range-1)]
        print(unsolved_ranges)
        curr_val = seed
        for key in key_order:
            print('moved to', key, len(unsolved_ranges))
            # print('unsolved ranges', unsolved_ranges)
            ranges = maps[key]
            next_unsolved = []
            for r in ranges:
                r_low = r[1]
                r_high = r[1] + r[2] - 1
                offset = r[0] - r[1]

                work = True
                # print('start work loop')
                while work:
                    # print('restart work loop')
                    work = False

                    to_pop = []
                    to_reprocess = []
                    for ur in unsolved_ranges:
                        print('working on range', ur, 'offset', offset)
                        ur_low = ur[0]
                        ur_high = ur[1]
                        if (r_low <= ur_low <= r_high) or (r_low <= ur_high <= r_high):
                            to_pop.append(ur)
                            print('to_pop', to_pop)

                            print(ur, 'within range', r_low, r_high)
                            if (r_low <= ur[0]) and (r_high >= ur[1]):
                                print('  fits fully inside')
                                # print(ur_low, ur_high, offset, (ur_low+offset, ur_high+offset))
                                next_unsolved.append((ur_low+offset, ur_high+offset))
                            elif r_low <= ur_low:
                                print('  overlaps on left', ur_low, r_high)
                                to_reprocess.append((r_high+1, ur_high))
                                next_unsolved.append((ur_low+offset, r_high+offset))
                            else:
                                print('  overlaps on right', r_low, ur_high)
                                to_reprocess.append((ur_low, r_low-1))
                                next_unsolved.append((r_low+offset, ur_high+offset))
                            work = True
                    # print((('to_pop', to_pop, 'to_reprocess', to_reprocess, 'next_unsolved', next_unsolved)))
                    # input(('to_pop', to_pop, 'to_reprocess', to_reprocess, 'next_unsolved', next_unsolved))
                    # if next_unsolved and min(next_unsolved)[0] == 0:
                    #     input('wtf')

                    for p in to_pop:
                        unsolved_ranges.remove(p)

                    for p in to_reprocess:
                        unsolved_ranges.append(p)
                # print('end work loop')
            unsolved_ranges += next_unsolved
            unsolved_ranges = list(set(unsolved_ranges))
            # print('wuh', unsolved_ranges, r)

            print('unsolved_ranges for seed', seed, unsolved_ranges)

            acc = 0
            for r in unsolved_ranges:
                acc += r[1] - r[0] + 1
            print('acc', acc, '==', seed_range)
            # assert acc == seed_range

        lowest = min(lowest, min(unsolved_ranges)[0])
        print(lowest)
        print('breaking after seed 0')
        break

        # lowest = min(lowest, curr_val)
    return lowest
# 7105488 too low
# 20358600 too high 20358599
# 20358599


def p2_rewrite():
    seeds = [int(i) for i in data[0].split(':')[1].strip().split()]
    # print(seeds)
    maps = defaultdict(list)
    for block in data[1:]:
        block = block.split('\n')
        map_name = block[0].split()[0]
        for line in block[1:]:
            line = [int(i) for i in line.split()]
            maps[map_name].append(line)
    # print(seeds, maps)
    key_order = maps.keys()
    lowest = INF

    it = iter(seeds)
    for seed_start in it:
        print('\n\nseed', seed_start)
        seed_range = next(it)
        seed_end = seed_start + seed_range - 1
        print(seed_start, seed_end)

        for key in key_order:
            source_ranges = maps[key]

            for source_range in source_ranges:
                source_start = source_range[1]
                source_end = source_start + source_range[2] - 1
                print('comparing seed range', seed_start, seed_end, 'to', source_start, source_end)

# for r in ranges:
            #     if r[1] <= curr_val <= (r[1] + r[2]):
            #         # print('in range', r)
            #         offset = r[0] - r[1]
            #         # print('offset', offset)
            #         curr_val = r[0] - r[1] + curr_val
            #         # print('next = ', curr_val)
            #         break
        lowest = min(lowest, curr_val)
    return lowest

setday(5)

with open_default() as file:
    data = [block for block in file.read().strip().split('\n\n')]
# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

print('part1:', p1() )
# print('part2:', p2_bruteforce() )
print('part2:', p2() )
