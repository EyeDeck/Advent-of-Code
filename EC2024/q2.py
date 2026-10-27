from ec import *


def p1():
    data = parse_lines(1)
    words = data[0].split(':')[1].split(',')
    inscription = data[2]
    return sum(inscription.count(word) for word in words)


def p2():
    data = parse_lines(2)
    words = data[0].split(':')[1]
    words = set((words + ',' + words[::-1]).split(','))
    inscription = ' '.join(data[2:])
    # print(words, inscription)
    mask = [0 for _ in range(len(inscription))]
    for word in words:
        w_len = len(word)
        start = 0
        while True:
            start = inscription.find(word, start)
            if start == -1:
                break
            mask[start:start+w_len] = [1] * w_len
            start += 1
    # print(mask)
    return sum(mask)


def p3():
    data = parse_lines(3)
    words = data[0].split(':')[1].split(',')

    # adapted from parse_grid()
    grid = {}
    inverse = defaultdict(list)
    unique = {}
    non_unique = set()
    for y, line in enumerate(data[2:]):
        for x, c in enumerate(line):

                grid[x, y] = c

                inverse[c].append((x, y))

                if c in unique:
                    del unique[c]
                    non_unique.add(c)
                elif c not in non_unique:
                    unique[c] = (x, y)

    to_search = grid.keys()
    maxdim = vadd(max(to_search), (1,1))
    found = set()

    def check_pos(grid, pos, direction, match, maxdim):
        s = set()
        for i, char in enumerate(match):
            # enables vertical wrapping too (oops)
            # coord = vmod(vadd(pos, vmul((i,i), DIRS[direction])), maxdim)

            coord = vadd(pos, vmul((i,i), DIRS[direction]))
            coord = (coord[0] % maxdim[0], coord[1])
            if coord[1] < 0 or coord[1] >= maxdim[1]:
                return False

            grid_char = grid[coord]
            if grid_char != char:
                return False
            s.add(coord)
        return s

    for pos in to_search:
        for word in words:
            for i in range(4):
                r = check_pos(grid, pos, i, word, maxdim)
                if r:
                    found |= r

    if verbose:
        print_2d('.', {k:v for k,v in grid.items() if k in found})
    return len(found)


if __name__ == '__main__':
    setquest(2)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
