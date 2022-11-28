#inp = [int(i) for i in open("d8.txt").read().split()]

# Alt big boi input (vanilla python list slicing takes literal hours, numpy takes a few seconds):
import numpy as np
inp = np.array([int(i) for i in open("d8-bb.txt").read().split()])

def parse(a):
	nodes = a[0]
	metadata = a[1]
	if (nodes == 0):
		return(metadata+2, sum(a[2:(2+metadata)]))
	else:
		l, v = 2, 0
		for i in range(nodes):
			rl, rv = parse(a[l:])
			l += rl
			v += rv
		v += sum(a[(l):(l+metadata)])
		return(l+metadata, v)

def parse2(a):
	nodes = a[0]
	metadata = a[1]
	if (nodes == 0):
		return(sum(a[2:(2+metadata)]))
	else:
		l, v = 2, 0
		nodeList = []
		for i in range(nodes):
			rl, rv = parse(a[l:])
			nodeList.append(a[l:l+rl])
			l += rl
		metaList = a[l:l+metadata]
		
		for n in metaList:
			if (n <= len(nodeList)):
				v += parse2(nodeList[n-1])
		
		return(v)

print(parse(inp)[1])
print(parse2(inp))