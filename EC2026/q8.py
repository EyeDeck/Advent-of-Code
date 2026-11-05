from ec import *

HEX_ADAPTER = [
    (-1, -1),
    (1, -1),
    (2, 0),
    (1, 1),
    (-1, 1),
    (-2, 0),
]

ARROWS = '↘↙←↖↗→'

def p1():
    grid, inverse, unique = parse_grid(1)

    grid = {k:int(v) for k,v in grid.items() if k not in inverse['.']}

    tl = set()
    for point in grid:
        if vadd(HEX_ADAPTER[2], point) not in grid:
            tl.add(point)

    print_2d(' ', grid, {k:'#' for k in tl})
    print()

    shade = {}
    for point in tl:
        highest = 0
        while point:
            if grid[point] > highest:
                highest = grid[point]
                shade[point] = grid[point]
            highest = max(0, highest-1)
            neighbor = vadd(HEX_ADAPTER[5], point)
            if neighbor in grid:
                point = neighbor
            else:
                point = None

    print_2d(' ', shade)

    return len(shade)


def p2():
    grid, inverse, unique = parse_grid(3)

    grid = {k:int(v) for k,v in grid.items() if k not in inverse['.']}

    seeds = {}
    acc_energy = 0
    acc_warriors = 0
    for step in range(1_000_000):
        shade = {}
        dir = step % 6
        curr_edge = set()
        for point in grid:
            if vadd(HEX_ADAPTER[dir], point) not in grid:
                curr_edge.add(point)

        for point in curr_edge:
            highest = 0
            while point:
                if grid[point] in seeds:
                    continue
                elif grid[point] > highest:
                    highest = grid[point]
                    shade[point] = grid[point]
                highest = max(0, highest-1)
                neighbor = vadd(HEX_ADAPTER[dir-3], point)
                if neighbor in grid:
                    point = neighbor
                else:
                    point = None

        acc_energy += len(shade)

        new_seeds = {}
        for k,v in seeds.items():
            if v == 1:
                grid[k] = 1
            else:
                new_seeds[k] = v-1

        seeds = new_seeds

        new_warriors = 0
        for point, v in shade.items():
            if v == 9:
                new_warriors += 1
                grid[point] = 0
                seeds[point] = 3
            else:
                grid[point] += 1

        acc_warriors += new_warriors

        if acc_warriors >= 100000:
            return acc_energy

        # print(f'Round: {step+1}\nDirection: {ARROWS[dir]}\nEnergy: {len(shade)}\nNew warriors: {new_warriors}\n')
        # print_2d(' ', shade, {vadd(HEX_ADAPTER[dir], k):'#' for k in curr_edge})
        # input()

    return


def p3():
    data = parse_lines(3)

    return


if __name__ == '__main__':
    setquest(8)

    # print('part1:', p1())
    # print('part2:', p2())
    print('part3:', p2())
