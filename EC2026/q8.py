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


def parse_input(n):
    grid, inverse, unique = parse_grid(n)
    return {k: int(v) for k, v in grid.items() if k not in inverse['.']}


def get_edge(direction, grid):
    edge = set()
    for point in grid:
        if vadd(HEX_ADAPTER[direction], point) not in grid:
            edge.add(point)
    return edge


def get_shade(direction, grid, seeds):
    edge = get_edge(direction, grid)
    shade = {}

    for point in edge:
        highest = 0
        while point:
            if grid[point] in seeds:
                continue
            elif grid[point] > highest:
                highest = grid[point]
                shade[point] = grid[point]
            highest = max(0, highest - 1)
            neighbor = vadd(HEX_ADAPTER[direction - 3], point)
            if neighbor in grid:
                point = neighbor
            else:
                point = None

    return shade


def gen_sunlight_overlay(direction, grid):
    sunlight = {}
    for i in range(1, 4):
        offset = vmul((i, i), HEX_ADAPTER[direction])
        sunlight |= {vadd(offset, k): ARROWS[direction] for k in get_edge(direction, grid)}
    return sunlight


def p1():
    grid = parse_input(1)

    shade = get_shade(0, grid, set())

    if verbose:
        print_2d('.', shade, gen_sunlight_overlay(0, grid))

    return len(shade)


def p2():
    grid = parse_input(2)

    acc = 0
    for i in range(6):
        shade = get_shade(i, grid, set())

        if verbose:
            print_2d('.', shade, gen_sunlight_overlay(i, grid))
            print()
        acc += len(shade)

    return acc


def p3():
    grid = parse_input(3)

    seeds = {}
    acc_energy = 0
    acc_warriors = 0
    for step in range(1_000_000):
        direction = step % 6

        shade = get_shade(direction, grid, seeds)

        acc_energy += len(shade)

        new_seeds = {}
        for k, v in seeds.items():
            if v == 1:
                grid[k] = 1
            else:
                new_seeds[k] = v - 1
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

        if verbose:
            print(f'Round: {step + 1}\nDirection: {ARROWS[direction]}\nEnergy: {len(shade)}\nNew warriors: {new_warriors}\n')
            print_2d('.', shade, gen_sunlight_overlay(direction, grid))
            if do_step:
                input()

    return


if __name__ == '__main__':
    setquest(8)

    do_step = '-s' in sys.argv or '--step' in sys.argv

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
