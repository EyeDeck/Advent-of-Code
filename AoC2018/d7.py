inpHandle = open("d7.txt")
inp = inpHandle.readlines()
inpHandle.close()

from collections import defaultdict
import string

def p1():
	reqs = defaultdict(list)
	steps = set()
	done = []

	for line in inp:
		s = line[5]
		r = line[36]
		reqs[r].append(s)
		steps.add(s)
		steps.add(r)

	steps = sorted(steps)

	while len(steps):
		for s in steps:
			if (len(reqs[s]) == 0):
				done.append(s)
				steps.remove(s)
				for k,v in reqs.items():
					if (s in v):
						v.remove(s)
				break
	return(''.join(done))

def p2():
	reqs = defaultdict(list)
	steps = set()
	queue = defaultdict(int)
	done = []

	for line in inp:
		s = line[5]
		r = line[36]
		reqs[r].append(s)
		steps.add(s)
		steps.add(r)

	steps = sorted(steps)
	
	# time to activate MAXIMUM OVERPAJEET
	seconds = 0
	while (len(steps) or len(queue)):
		a = False
		if (len(queue) < 5):
			for s in steps:
				if (len(reqs[s]) == 0):
					queue[s] = 61 + string.ascii_uppercase.index(s)
					steps.remove(s)
					a = True
					break
		if (a):
			continue
		
		toPop = []
		for k,_ in queue.items():
			queue[k] -= 1
			if (queue[k] == 0):
				done.append(k)
				toPop.append(k)
				for k2,v2 in reqs.items():
					if (k in v2):
						v2.remove(k)
		for k in toPop:
			queue.pop(k)
		
		seconds += 1
	return(seconds)

print(p1())
print(p2())