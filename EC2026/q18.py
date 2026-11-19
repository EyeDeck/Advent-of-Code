from ec import *


def p1():
    data = parse_lines(1, get_ints)
    grid = {}
    max_x, max_y = 0, 0
    for line in data:
        x, y = line
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        for y_pos in range(y):
            grid[line[0], y_pos] = '#'

    # print_2d(' ', {vmul(k, (1, -1)):v for k,v in grid.items()})

    for y in range(max_y + 1):
        last = -1
        for x in range(max_x + 1):
            if (x,y) not in grid:
                continue

            # print_2d(' ', grid, {(x,y):'!'})

            if last < 0:
                last = x+1
            else:
                # print(x, last)
                for offset in range(x, last, -1):
                    grid[offset-1, y] = '='
                last = x+1


    print_2d(' ', {vmul(k, (1, -1)):v for k,v in grid.items()})


    return len(grid)


def p2():
    data = parse_lines(3, get_ints)

    grid = {}
    max_x, max_y = 0, 0
    for line in data:
        x, y, w = line
        max_x = max(max_x, x+w-1)
        max_y = max(max_y, y)
        for y_pos in range(y):
            grid[line[0], y_pos] = '#'
        if w > 1:
            for y_pos in range(y):
                grid[line[0]+w-1, y_pos] = '#'
        # for w_pos in range(w):
        #     print(line)
        #     for y_pos in range(y):
        #         grid[line[0]+w_pos-1, y_pos] = '#'

    # print_2d(' ', {vmul(k, (1, -1)):v for k,v in grid.items()})

    for y in range(max_y + 1):
        last = -1
        for x in range(max_x + 1):
            if (x,y) not in grid:
                continue

            # print_2d(' ', grid, {(x,y):'!'})

            if last < 0:
                last = x + 1
            else:
                # print(x, last)
                for offset in range(x, last, -1):
                    grid[offset-1, y] = '='
                last = x + 1

    print_2d(' ', {vmul(k, (1, -1)):v for k,v in grid.items()})
    # print('scaled to 100x50:')
    # print_2d(' ', {(k[0]//(max_x//100), (k[1]*-1)//(max_y//50)):v for k,v in grid.items()})


    return len(grid)


# was pretty sure part 3 was gonna basically be part 1 with big numbers
# almost wrote it properly from the start but decided I didn't wanna overinvest...
def p3():
    data = parse_lines(3, get_ints)

    parsed = []
    for line in data:
        x, y, w = line
        parsed.append((x,y))
        if w > 1:
            parsed.append((x+w-1,y))

    parsed.sort()
    print(parsed)

    def fill_square(grid, x_start, y_start, x_end, y_end):
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                grid[x, y] = '#'


    grid = {}

    max_y = 0
    rising_acc = 0
    last_x, last_y = 0, 0
    for line in parsed:
        x, y = line
        if y >= last_y:
            print('\t', x, y)
            max_y = max(max_y, y)

            rising_acc += (x-last_x) * last_y
            # fill_square(grid, last_x, 0, x, last_y)

            last_x = x
            last_y = y
    print(rising_acc)



    last_x_rising = last_x

    falling_acc = 0
    last_x, last_y = parsed[-1][0], 0
    print(last_x, last_y)
    for line in reversed(parsed):
        x, y = line
        if y >= last_y:
            print('\t', x, y)

            # falling_acc += (last_x - last_x_rising) * y

            falling_acc += (last_x - x) * last_y

            # fill_square(grid, x, 0, last_x, last_y)

            last_x = x
            last_y = y
            if y == max_y:
                falling_acc += y
                break
    print(falling_acc)

    print(rising_acc+falling_acc)

    # print_2d(' ', grid)
    # print(len(grid))

    return rising_acc+falling_acc



if __name__ == '__main__':
    setquest(18)

    # print('part1:', p1())
    # print('part2:', p2())
    print('part3:', p3())
