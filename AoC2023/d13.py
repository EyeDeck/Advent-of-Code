from aoc import *

def solve(part2):
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
        for vert_or_horiz in range(2):
            height_or_width = height if vert_or_horiz == 0 else width

            for n in range(1, height_or_width+1):
                off = 0
                diffs = 0
                for n2 in range(n-1,max(-1, n-(height_or_width-n+2)),-1):
                    a = get_strip(board, n+off, width, height, vert_or_horiz)
                    b = get_strip(board, n2, width, height, vert_or_horiz)

                    if part2:
                        cmb = [0 if a[i] == b[i] else 1 for i in range(len(a))]
                        diffs += sum(cmb)
                        if diffs > 1:
                            break
                    else:
                        if a != b:
                            break

                    off += 1
                else:
                    if not part2 or diffs == 1:
                        return n * (100 if vert_or_horiz == 0 else 1)

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
            print('Summary:', result, '\n')

        acc += result

    return acc


setday(13)

with open_default() as file:
    boards = [line.strip() for line in file.read().split('\n\n')]

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', solve(False) )
print('part2:', solve(True) )
