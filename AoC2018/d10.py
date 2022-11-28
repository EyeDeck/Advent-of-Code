import re
from operator import itemgetter

# minx, miny, maxx, maxy
def findbounds(points):
	return [min(points, key=itemgetter(0))[0], min(points, key=itemgetter(1))[1], max(points, key=itemgetter(0))[0], max(points, key=itemgetter(1))[1]]

def zeroalign(points):
	bounds = findbounds(points)
	aligned = []
	for i in range(len(parsed)):
		aligned.append([parsed[i][0] + (bounds[0]*-1), parsed[i][1] + (bounds[1]*-1), parsed[i][2], parsed[i][3]])
	return aligned

def render(points):
	aligned = zeroalign(points)
	bounds = findbounds(aligned)
	board = [["." for i in range(bounds[3]+1)] for i in range(bounds[2]+1)]
	for point in aligned:
		board[point[0]][point[1]] = "#"
	tostr = []
	for i in range(len(board[0])):
		for j in range(len(board)):
			tostr.append(board[j][i])
		tostr.append("\n")
	return "".join(tostr)

def step(points, mod):
	for i in range(len(points)):
		points[i][0] += points[i][2] * mod
		points[i][1] += points[i][3] * mod
	return points

parsed = [[int(n) for n in re.sub("[a-zA-Z=<>,]", "", i).split()] for i in open("d10.txt").readlines()]
def p1():
	seconds = 0
	lastbounds = findbounds(zeroalign(parsed))
	while True:
		bounds = findbounds(zeroalign(parsed))
		if (bounds[2]*bounds[3] > lastbounds[2]*lastbounds[3]):
			break
		board = step(parsed, 1)
		lastbounds = bounds
		seconds += 1
	print(render(step(parsed,-1)))
	print("Took",seconds-1,"seconds.")

p1()