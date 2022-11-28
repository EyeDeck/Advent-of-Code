inp = open("d20.txt").read()

# this feels like an abortion of code but I genuinely can't think of a simpler way to do this
def rparse(s):
	o = []
	toparse = []
	pct = 0
	orify = 0
	for c in s:
		if c in {"N","S","E","W"}:
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
		return(o2)
	else:
		return(o)

def traverse(inp, depth):
	depth += 1
	longest = 0
	stack = []
	for move in inp:
		if isinstance(move,list):
			longest = max(longest, traverse(move,depth))
		else:
			stack.append(move)
			if len(stack) > 1 and {stack[-1], stack[-2]} in reverse:
				stack = stack[0:-2]
	#print(" "*depth, "longest", length)
	return(len(stack) + longest)

def test(inp):
	parsed = rparse(inp[0][1:-1])
	maxlen = traverse(parsed,-1)
	print("PASSED:" if maxlen == inp[1] else "FAILED:", "Tested regex, got", maxlen, "expected", inp[1])

tests = [
	("^WNE$", 3),
	("^ENWWW(NEEE|SSE(EE|N))$", 10),
	("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18),
	("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23),
	("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31),
	(open("d20-e.txt").read(), 3958),
	(open("d20-mb.txt").read(), 1600),
	(open("d20-bb.txt").read(), 9982),
	(inp, 4247),
]

reverse = [{"N","S"}, {"E","W"}]

for t in tests:
	test(t)