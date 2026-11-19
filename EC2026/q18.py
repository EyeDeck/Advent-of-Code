from ec import *


def fill_square(grid, x_start, y_start, x_end, y_end, char):
    if not verbose or y_end >= 255:
        return
    for x in range(x_start, x_end + 1):
        for y in range(y_start, y_end):
            grid[x, y] = char


def solve(part):
    data = parse_lines(part, get_ints)

    parsed = []
    for line in data:
        if len(line) == 2:
            x, y = line
            w = 1
        else:
            x, y, w = line

        parsed.append((x, y))
        if w > 1:
            parsed.append((x + w - 1, y))

    parsed.sort()

    grid = {}

    max_y = 0
    acc = 0
    last_x, last_y = 0, 0
    for line in parsed:
        x, y = line
        if y >= last_y:
            max_y = max(max_y, y)

            acc += (x - last_x) * last_y

            fill_square(grid, last_x, 0, x, last_y, '#')

            last_x = x
            last_y = y

    last_x, last_y = parsed[-1][0], 0

    for line in reversed(parsed):
        x, y = line
        if y >= last_y:
            acc += (last_x - x) * last_y

            fill_square(grid, x, 0, last_x, last_y, '#')

            last_x = x
            last_y = y
            if y == max_y:
                acc += y
                break

    if verbose and grid:
        print_2d(' ', {vmul(k, (1, -1)): v for k, v in grid.items()})

    return acc


if __name__ == '__main__':
    setquest(18)

    print('part1:', solve(1))
    print('part2:', solve(2))
    print('part3:', solve(3))
