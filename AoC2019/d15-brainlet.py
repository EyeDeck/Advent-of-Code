import copy
import sys

import numpy as np

def render(bd):
    print(np.array2string(bd, max_line_width=200, separator=' ', threshold=1000, edgeitems=1000,
                          formatter={'str_kind': lambda x: x}), end='\n')

f = 'd15-brainlet.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

parsed = np.array([[z for z in x.strip()] for x in open(f).readlines()])
print(parsed)

did_work = True
ticks = 0
while did_work:
    did_work = False

    nxt = copy.deepcopy(parsed)
    for x, line in enumerate(parsed):
        for y, char in enumerate(line):
            if char == '@':
                if parsed[x-1][y] == '.':
                    nxt[x-1][y] = '@'
                    did_work = True
                if parsed[x+1][y] == '.':
                    nxt[x + 1][y] = '@'
                    did_work = True
                if parsed[x][y-1] == '.':
                    nxt[x][y-1] = '@'
                    did_work = True
                if parsed[x][y+1] == '.':
                    nxt[x][y+1] = '@'
                    did_work = True
    print(render(parsed))
    ticks += 1
    input(ticks)
    parsed = nxt
print(ticks)

# not 211
# 395 too high