from aoc import *

def p1():
    width = max(grid.keys(), key=itemgetter(0))[0]
    height = max(grid.keys(), key=itemgetter(1))[1]
    for n in range(height):
        for x in range(width+1):
            for y in range(1,height+1):
                if grid[x,y] == 'O' and grid[x,y-1] == '.':
                    grid[x,y] = '.'
                    grid[x,y-1] = 'O'
    acc = 0
    for k,v in grid.items():
        if v == 'O':
            acc += height-k[1]+1
    print_2d(' ', grid)
    return acc


def p2():
    width = max(grid.keys(), key=itemgetter(0))[0]
    height = max(grid.keys(), key=itemgetter(1))[1]
    # cycles = [(0, height+1, 1,  1, width+1, 1,  0, -1),
    #           (width-1, -1, -1,      1,0), (0,1), (-1,0)]

    def spin(grid):
        # north
        for n in range(height):
            for x in range(width+1):
                for y in range(1, height+1):
                    if grid[x,y] == 'O' and grid[x,y-1] == '.':
                        grid[x,y] = '.'
                        grid[x,y-1] = 'O'

        # west
        for n in range(width):
            for x in range(1, width+1):
                for y in range(0, height+1):
                    if grid[x, y] == 'O' and grid[x-1, y] == '.':
                        grid[x, y] = '.'
                        grid[x-1, y] = 'O'

        # south
        for n in range(height):
            for x in range(0, width+1):
                for y in range(height-1, -1, -1):
                    if grid[x,y] == 'O' and grid[x,y+1] == '.':
                        grid[x,y] = '.'
                        grid[x,y+1] = 'O'

        # east
        for n in range(width):
            for x in range(width-1, -1, -1):
                for y in range(0, height+1):
                    if grid[x, y] == 'O' and grid[x+1, y] == '.':
                        grid[x, y] = '.'
                        grid[x+1, y] = 'O'

    seen = {}
    for i in range(1000000000):
        print('\n', i)
        spin(grid)
        print_2d(' ', grid)
        hashable = str(grid)
        if hashable in seen.keys():
            last, weight = seen[hashable]
            cycle_len = i - last
            print('at cycle', i, 'last seen', last, 'cycle len', cycle_len)
            print(1000000000 % cycle_len)
            print(seen.values())
            ans = [x for x in seen.values()][((1000000000 - last) % cycle_len) + last -1]
            return ans

        acc = 0
        for k, v in grid.items():
            if v == 'O':
                acc += height - k[1] + 1

        seen[hashable] = (i, acc)
    print(seen)

# not 102837
# not 102851
# 102829!

setday(14)

grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
