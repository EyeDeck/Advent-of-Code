inp = open("d17.txt").read()
 
import re, numpy as np
from PIL import Image
 
def renderboard(board,loc="d17.png"):
    palette = [0,0,0, 0xFF,0xA0,0x66, 0x14,0x66,0xFF, 0x38,0x7D,0xFF, 0,0xFF,0xDD]
   
    img = Image.fromarray(board, "P")
    img.putpalette(palette)
    img.save(loc)
 
def step(board):
    for i in range(len(activewater)):
        w = activewater.pop()
        if (w[0]+1 > bounds[3]):
            board[w[0]][w[1]] = 3
            continue
        down = board[w[0]+1][w[1]]
        if down not in solid:
            # falling
            activewater.add((w[0]+1,w[1]))
            board[w[0]][w[1]] = 3
        else:
            # hit something, so check if there's a basin to fill
            flat = [0,0]
            enclosed = True
            while True:
                if (board[w[0]][w[1]+flat[0]-1] in solid):
                    #print("left bound at",flat)
                    break
                elif (board[w[0]+1][w[1]+flat[0]-1] not in solid):
                    #print("found a hole on the left")
                    activewater.add((w[0], w[1]+flat[0]-1))
                    enclosed = False
                    break
                else:
                    #print("lb",flat)
                    flat[0] -= 1
           
            while True:
                if (board[w[0]][w[1]+flat[1]+1] in solid):
 
                    #print("right bound at",flat)
                    break
                elif (board[w[0]+1][w[1]+flat[1]+1] not in solid):
                    #print("found a hole on the right")
                    activewater.add((w[0], w[1]+flat[1]+1))
                    enclosed = False
                    break
                else:
                    #print("rb",flat)
                    flat[1] += 1
           
            if enclosed:
                # the thing we hit is enclosed, so make this all standing water and reset our activewater 1 tick up the flow
                for i in range(w[1]+flat[0],w[1]+flat[1]+1):
                    board[w[0]][i] = 2
                activewater.add((w[0]-1,w[1]))
            else:
                # there's a hole, so make the range we found flowing water and let the new activewater entries tick
                for i in range(w[1]+flat[0],w[1]+flat[1]+1):
                    board[w[0]][i] = 3
 
ud = sorted([[int(j) for j in i] for i in re.compile("x=(\d+), y=(\d+)\.\.(\d+)").findall(inp)]) # vertical ranges
lr = sorted([[int(j) for j in i] for i in re.compile("y=(\d+), x=(\d+)\.\.(\d+)").findall(inp)]) # horiz ranges
 
bounds = (min(500,ud[0][0]), min(0, lr[0][0]), ud[-1][0], lr[-1][0])
xoffset = bounds[0] - 1
miny = 0x7FFFFFFF
 
boundsoffset = (bounds[0]-xoffset, bounds[1], bounds[2]-xoffset, bounds[3])
 
empty, clay, waters, waterf, spring = 0, 1, 2, 3, 4
solid = [1,2]
 
board = np.zeros((bounds[3]-bounds[1]+1, bounds[2]-bounds[0]+3), dtype=np.uint8)
#print(len(board), len(board[0]))
#print(bounds)
 
for line in ud:
    x = line[0]
    for y in range(line[1],line[2]+1):
        if (y < miny):
            miny = y
        board[y][x-xoffset] = 1
 
for line in lr:
    y = line[0]
    if (y < miny):
        miny = y
    for x in range(line[1],line[2]+1):
        board[y][x-xoffset] = 1
 
board[0][500-xoffset] = 4
activewater = {(1,500-xoffset)}
 
i = 0
while activewater:
    step(board)
    #renderboard(board,"d17\\frame" + str(i).zfill(4) + ".png")
    i += 1
 
p1 = sum([sum([1 if x == 2 or x == 3 else 0 for x in y]) for y in board[miny:]])
p2 = sum([sum([1 if x == 2 else 0 for x in y]) for y in board[miny:]])
 
print("P1", p1)
print("P2", p2)
 
renderboard(board)