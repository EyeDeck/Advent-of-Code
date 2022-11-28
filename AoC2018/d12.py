inpHandle = open("d12.txt")
inp = inpHandle.readlines()
inpHandle.close()

def bltoint(i):
	return sum(1<<j for j,k in enumerate(i) if k)

def step(s, rules, zoffset):
	ts = s.copy()
	for i in range(3):
		ts.insert(0,False)
		ts.append(False)
	
	zoffset -= 1
	
	ns = []
	for i in range(2,len(ts)-1):
		ns.append(rules[bltoint(ts[i-2:i+3])])
		# print("got",rules[bltoint(ts[i-2:i+3])],"for",ts[i-2:i+3])
	while (ns[0] == False):
		ns.pop(0)
		zoffset += 1
	while (ns[-1] == False):
		ns.pop()
	
	return(ns, zoffset)

def scoreinput(state, rules, iterations):
	tstate = state.copy()
	zoffset = 0
	for i in range(iterations):
		newstate, newzoffset = step(tstate, rules, zoffset)
		print(i+1, zoffset, "".join(["#" if j == True else "." for j in newstate]))
		if (newstate == tstate):
			zoffset += (iterations-i)*(newzoffset-zoffset)
			break
		tstate = newstate
		zoffset = newzoffset
	
	score = 0
	for i in range(len(tstate)):
		if (tstate[i]):
			score += i + zoffset
	return score

state = [True if i == "#" else False for i in inp[0][15:-1]]
# rules = ([i[0:5] for i in inp[2:]], [i[9] for i in inp[2:]])
rules = dict()
for i in range(32):
	rules[i] = False
for i in inp[2:]:
	rules[bltoint([True if j == "#" else False for j in [k for k in i[0:5]]])] = True if i[9] == "#" else False
#print(rules)

print("Part 1:", scoreinput(state, rules, 20))
print("Part 2:", scoreinput(state, rules, 50000000000))
