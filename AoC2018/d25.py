inp = open("d25.txt").readlines()
parsed = [tuple([int(i) for i in l.split(",")]) for l in inp]

def dist(a,b):
	return(abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3]))

def mergecons(cs):
	for c in range(len(cs)):
		for s in cs[c]:
			for c2 in range(len(cs)):
				for s2 in cs[c2]:
					if c == c2:
						continue
					if dist(s, s2) <= 3:
						return (c, c2)
	return False

constellations = [set([s]) for s in parsed]

while True:
	tomerge = mergecons(constellations)
	if tomerge:
		constellations[tomerge[0]] = constellations[tomerge[0]] | constellations[tomerge[1]]
		del constellations[tomerge[1]]
	else:
		break

print(len(constellations))