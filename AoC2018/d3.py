inputHandle = open("d3.txt")
input = inputHandle.readlines()
inputHandle.close()

import re

xMax = 1000
yMax = 1000

def p1():
	sheet = [[0] * xMax for i in range(yMax)]
	overlap = 0
	
	exp = re.compile("@ (\d+),(\d+): (\d+)x(\d+)")
	for claim in input:
		x,y,w,h = exp.findall(claim)[0]
		for i in range(int(w)):
			for j in range(int(h)):
				sheet[int(x)+i][int(y)+j] += 1
	
	for i in range(xMax):
		for j in range(yMax):
			if (sheet[i][j] > 1):
				overlap += 1
	
	return overlap
	
def p2():
	sheet = [[0] * xMax for i in range(yMax)]
	
	exp = re.compile("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
	for claim in input:
		n,x,y,w,h = exp.findall(claim)[0]
		for i in range(int(w)):
			for j in range(int(h)):
				sheet[int(x)+i][int(y)+j] += 1
	
	for claim in input:
		n,x,y,w,h = exp.findall(claim)[0]
		bad = False
		for i in range(int(w)):
			for j in range(int(h)):
				if (sheet[int(x)+i][int(y)+j] != 1):
					bad = True
		
		if (bad == False):
			return n

print(p1())
print(p2())
# This day felt particularly quick and dirty (p2 took me about 3 minutes)