inp = open("d20.txt").read()

import collections, numpy as np
from operator import itemgetter

# this feels like an abortion of code but I genuinely can't think of a simpler way to do this
def rparse(s):
	o = []
	toparse = []
	pct = 0
	orify = 0
	for c in s:
		if c in "NSEW":
			if pct == 0:
				o.append(c)
			else:
				toparse.append(c)
		elif c == "(":
			if pct == 0:
				None
			else:
				toparse.append(c)
			pct += 1
		elif c == ")":
			pct -= 1
			if pct == 0:
				o.append(rparse("".join(toparse)))
				toparse = []
			else:
				toparse.append(c)
		else: # |
			if pct == 0:
				orify = True
				o.append(c)
			else:
				toparse.append(c)
	if orify:
		o2 = [[]]
		for c in o:
			if c == "|":
				o2.append([])
			else:
				o2[-1].append(c)
		return o2
	else:
		return o

# stupid approach, but left here for posterity
#def traverse(inp, depth):
#	# print(depth, inp)
#	longest = 0
#	overmax = 0
#	stack = []
#	for move in inp:
#		if isinstance(move,list):
#			thislen, thisom = traverse(move, depth)
#			overmax += thisom
#			longest = max(longest, thislen)
#		else:
#			stack.append(move)
#			depth += 1
#			if len(stack) > 1 and {stack[-1], stack[-2]} in reverse:
#				stack = stack[0:-2]
#				depth -= 2
#			
#			if (depth > 1000):
#				overmax += 1
#	return len(stack) + longest, overmax

def makeboard(inp, points, pos):
	filladj(pos, points)
	for move in inp:
		if isinstance(move,list):
			makeboard(move, points, pos)
		else:
			pos = tuple(np.add(pos,dir[move]))
			points[pos] = dirdoors[move]
			pos = tuple(np.add(pos,dir[move]))
			points[pos] = "."
			filladj(pos, points)
	return(points)

def makeoverlay(coords, char):
	return {c:char for c in coords}

def filladj(coord, points):
	for x in [-1,1]:
		for y in [-1,1]:
			points[(x+coord[0],y+coord[1])] = "#"
	for d in dir.values():
		points.setdefault(tuple(np.add(coord, d)), "?")

def render(points, overlay=""):
	off = [0x7FFFFFFF,0x7FFFFFFF,-0x7FFFFFFF,-0x7FFFFFFF] #(minx, miny, maxx, maxy)
	for k in points.keys():
		off[0] = min(off[0], k[0])
		off[1] = min(off[1], k[1])
		off[2] = max(off[2], k[0])
		off[3] = max(off[3], k[1])
	bounds = (off[2] - off[0] + 1, off[3] - off[1] + 1)
	
	toprint = np.full(bounds, " ")
	for k,v in points.items():
		if k in overlay:
			toprint[k[0]-off[0]][k[1]-off[1]] = overlay[k]
		else:
			toprint[k[0]-off[0]][k[1]-off[1]] = v
	toprint = np.transpose(toprint)
	
	tostr = []
	for x in range(bounds[1]):
		for y in range(bounds[0]):
			tostr.append(toprint[x][y])
		tostr.append("\n")
	return "".join(tostr)


def bfs(board,start):
	seen = {start}
	stack = collections.deque([[start]])
	lenstack = collections.deque([0])
	longest, longestlen = None, None
	over1k = set()
	while stack:
		path = stack.popleft()
		len = lenstack.popleft()
		
		for d in dir.values():
			this = tuple(np.add(path[-1], d))
			if board[this] != "#" and this not in seen:
				thislen = len
				if board[this] in doors:
					thislen += 1
				if thislen >= 1000 and board[this] == ".":
					over1k.add(this)
				seen.add(this)
				stack.append(path + [this])
				lenstack.append(thislen)
				
				longest = stack[-1]
				longestlen = lenstack[-1]
		#if stack:
		#	print(lenstack[-1], render(board,makeoverlay(stack[-1], "~")))
		#	input()
	return longest, longestlen, over1k

# my first failed attempt at an algorithm was so shitty I ended up doing automated tests
tests = [
	#("^WNE$", 3),
	#("^ENWWW(NEEE|SSE(EE|N))$", 10),
	#("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18),
	#("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23),
	#("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31),
	#(open("d20-e.txt").read(), 3958),
	#(open("d20-mb.txt").read(), 1600, 391602),
	#(open("d20-bb.txt").read(), 9982, 15420052),
	(inp, 4247),
]

dir = {"N":(0,-1), "S":(0,1), "E":(1,0), "W":(-1,0)}
doors = {"-","—","|"}
dirdoors = {"N":"—", "S":"—", "E":"|", "W":"|"}
reverse = [{"N","S"}, {"E","W"}]

def test(inp, dbg):
	parsed = rparse(inp[0][1:-1])
	points = {(0,0):"X"}
	points = makeboard(parsed, points, (0,0))
	points = {k:"#" if v == "?" else v for k,v in points.items()}
	longestpath, doorct, over1k = bfs(points,(0,0))
	if dbg:
		print(render(points,{**makeoverlay(longestpath, "~"), **makeoverlay(over1k, "@")}))
		return "".join(["PASSED: " if doorct == inp[1] else "FAILED: ", " Tested regex, got ", str(doorct), ", expected ", str(inp[1]), "; ", str(len(over1k))])
	else:
		return "".join(["P1: ", str(doorct), "\nP2: ", str(len(over1k))])

for t in tests:
	print(test(t, True))
