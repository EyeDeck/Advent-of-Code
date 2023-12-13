from aoc import *

def p1():
    def get_strip(board, n, w, h, axis):
        """axis 0 = row, 1 = column"""
        r = []
        if axis == 0:
            for x in range(w+1):
                r.append(board[x, n])
        else:
            for y in range(h+1):
                r.append(board[n, y])
        return r

    def get_mirror(board, width, height):
        for y in range(1, height+1):
            # print('moved to row',y+1)
            off = 0
            # print(y-1,max(-1, y-(height-y+2)),-1)
            for y2 in range(y-1,max(-1, y-(height-y+2)),-1):
                # print('checking row', y+off+1, 'against row', y2+1)
                if get_strip(board, y+off, width, height, 0) != get_strip(board, y2, width, height, 0):
                    break
                off += 1
            else:
                if verbose:
                    print('found mirror', y * 100)
                return y * 100

        for x in range(1, width+1):
            # print('moved to col',x+1, x, width)
            off = 0
            # print(x-(width-x+2),x-1,-1)
            for x2 in range(x-1,max(-1, x-(width-x+2)),-1):
                # print('checking col', x+off+1, 'against col', x2+1)
                if get_strip(board, x+off, width, height, 1) != get_strip(board, x2, width, height, 1):
                    break
                off += 1
            else:
                if verbose:
                    print('found mirror', x)
                return x

    acc = 0
    for board in boards:
        board = board.split('\n')
        grid = {}
        for y, line in enumerate(board):
            for x, c in enumerate(line):
                grid[x, y] = c
        width =  max(grid.keys(), key=itemgetter(0))[0]
        height = max(grid.keys(), key=itemgetter(1))[1]

        result = get_mirror(grid, width, height)

        if verbose:
            if result < 100:
                overlay = {(result-1,       -1): '>', (result,       -1): '<',
                           (result-1, height+1): '>', (result, height+1): '<'}
            else:
                overlay = {(     -1, result//100-1): 'v', (     -1, result//100): '^',
                           (width+1, result//100-1): 'v', (width+1, result//100): '^'}
            print_2d(' ', grid, overlay)

        acc += result
        # input()

    return acc


def p2():
    def get_strip(board, n, w, h, axis):
        """axis 0 = row, 1 = column"""
        r = []
        if axis == 0:
            for x in range(w+1):
                r.append(board[x, n])
        else:
            for y in range(h+1):
                r.append(board[n, y])
        return r

    def get_mirror(board, width, height):
        for y in range(1, height+1):
            # print('moved to row',y+1)
            off = 0
            diffs = 0
            # print(y-1,max(-1, y-(height-y+2)),-1)
            for y2 in range(y-1,max(-1, y-(height-y+2)),-1):
                # print('checking row', y+off+1, 'against row', y2+1)

                a = get_strip(board, y+off, width, height, 0)
                b =  get_strip(board, y2, width, height, 0)
                cmb = [0 if a[i] == b[i] else 1 for i in range(len(a))]
                diffs += sum(cmb)
                if diffs > 1:
                    break
                off += 1
            else:
                if diffs == 1:
                    if verbose:
                        print('found mirror', y * 100)
                    return y * 100

        for x in range(1, width+1):
            # print('moved to col',x+1, x, width)
            off = 0
            diffs = 0
            # print(x-(width-x+2),x-1,-1)
            for x2 in range(x-1,max(-1, x-(width-x+2)),-1):
                # print('checking col', x+off+1, 'against col', x2+1)
                a = get_strip(board, x+off, width, height, 1)
                b = get_strip(board, x2, width, height, 1)
                cmb = [0 if a[i] == b[i] else 1 for i in range(len(a))]
                diffs += sum(cmb)
                if diffs > 1:
                    break
                off += 1
            else:
                if diffs == 1:
                    if verbose:
                        print('found mirror', x)
                    return x

    acc = 0
    for board in boards:
        board = board.split('\n')
        grid = {}
        for y, line in enumerate(board):
            for x, c in enumerate(line):
                grid[x, y] = c
        width =  max(grid.keys(), key=itemgetter(0))[0]
        height = max(grid.keys(), key=itemgetter(1))[1]

        result = get_mirror(grid, width, height)

        if verbose:
            if result < 100:
                overlay = {(result-1,       -1): '>', (result,       -1): '<',
                           (result-1, height+1): '>', (result, height+1): '<'}
            else:
                overlay = {(     -1, result//100-1): 'v', (     -1, result//100): '^',
                           (width+1, result//100-1): 'v', (width+1, result//100): '^'}
            print_2d(' ', grid, overlay)

        acc += result

    return acc


setday(13)

with open_default() as file:
    boards = [line.strip() for line in file.read().split('\n\n')]

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1() )
print('part2:', p2() )
