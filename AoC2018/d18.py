inp = open("d18.txt").readlines()
inp = [list(l.rstrip("\n")) for l in inp]

import numpy as np

def render(board):
	tostr = []
	for y in range(h):
		for x in range(w):
			tostr.append(str(board[y][x]))
		tostr.append("\n")
	return "".join(tostr)

rules = {
	".": lambda s : "|" if (s == "|").sum() >= 3 else ".",
	"|": lambda s : "#" if (s == "#").sum() >= 3 else "|",
	"#": lambda s : "#" if ((s == "#").sum() > 1 and (s == "|").sum() >= 1) else ".",
}

def step(b):
	newboard = np.full_like(b, ".")
	for y in range(h):
		for x in range(w):
			slice = b[max(0,y-1):min(h,y+2), max(0,x-1):min(w,x+2)]
			newboard[y][x] = rules[b[y][x]](slice)
	return newboard

board = np.array(inp)
w, h = len(board[0]), len(board)

ticks = 0
for i in range(10):
	board = step(board)
	ticks += 1
	print(render(board))
print("P1", (board == "|").sum() * (board == "#").sum())

# fuck it, can't be bothered to code nicely
# naively find cycle len (praying that it starts to happen after the first 500 cycles)
for i in range(500):
	board = step(board)
	print(render(board))
	ticks += 1

tofind = board.copy()
cyclelen = 0
for i in range(500):
	board = step(board)
	ticks += 1
	if np.array_equal(board, tofind):
		cyclelen = i + 1
		break
print("Cycle length is", cyclelen)

for i in range((1000000000 - ticks) % cyclelen):
	board = step(board)
	
print("P2", (board == "|").sum() * (board == "#").sum())
