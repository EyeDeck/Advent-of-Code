inp = open("d13-mb.txt").readlines()

import numpy as np

def parsecarts(board):
	carts = {}
	for x in range(len(board)):
		for y in range(len(board[x])):
			c = board[x][y]
			if c in "<>v^":
				carts[x,y] = (c,0)
				# a cheat that won't work with some valid inputs (though AOC doesn't seem to generate these)
				board[x][y] = " "
	return board, carts

def step(board, carts, crashes, stepct):
	for k,v in sorted(list(carts.items())):
		x,y = k
		if (k in carts):
			cart, step = carts.pop(k)
		else:
			continue
		
		next = (0,0)
		if cart == "^":
			next = (x,y-1)
		elif cart == ">":
			next = (x+1,y)
		elif cart == "v":
			next = (x,y+1)
		else: # cart == "<"
			next = (x-1,y)
		
		if next in carts:
			carts.pop(next)
			crashes.append((next,stepct))
		else:
			# board[x][y] = cart
			# print(x,y,v,board[next[0]][next[1]])
			nexttrack = board[next[0]][next[1]]
			if nexttrack == "+":
				if step == 0:
					cart = rotations[cart][0] # left
					step = 1
				elif step == 1:
					# straight
					step = 2
				else: # step == 2
					cart = rotations[cart][1] # right
					step = 0
			elif nexttrack == "\\":
				cart = rotations[cart][1 if cart in "<>" else 0]
			elif nexttrack == "/":
				cart = rotations[cart][1 if cart in "^v" else 0]
			
			carts[next] = (cart, step)
			
		# print(x,y,v)
	return(board, carts, crashes)

def render(board, carts):
	tostr = []
	for x in range(len(board[0])):
		for y in range(len(board)):
			c = board[y][x]
			if ((y,x) in carts):
				tostr.append(carts[(y,x)][0])
			else:
				tostr.append(c if c not in "-|" else " ")
			
		tostr.append("\n")
	return "".join(tostr)

inp = [l.rstrip("\n") for l in inp]

rotations = {"^":("<",">"),"<":("v","^"),"v":(">","<"),">":("^","v")}

board = np.rot90(np.flipud(np.array([c for c in [list(l) for l in inp]])),3)
crashes = []
board, carts = parsecarts(board)

stepct = 1
while(len(carts) != 1):
	stepct += 1
	step(board, carts, crashes, stepct)
	# print(render(board, carts))
	# input()
print("Detected the following crashes:")
for c in crashes:
	print(c[0], "on tick", c[1])
print("Final remaining cart:", carts.popitem())