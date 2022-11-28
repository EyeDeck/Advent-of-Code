inp = 123456789

def getrecipes(inp, index, count):
	recipes = bytearray([int(i) for i in str(inp)])
	target = bytearray([int(i) for i in str(index)])
	tlen = len(target)
	elves = [0,1]
	p1, p2 = None, None
	while p1 == None or p2 == None:
		if p1 == None and len(recipes) > index+count:
			p1 = "".join([str(i) for i in recipes[index:index+count]])
		if p2 == None:
			for i in range(1,2):
				if recipes[-i-(tlen):-i] == target:
					p2 = len(recipes) - tlen - i
		new = sum([recipes[e] for e in elves])
		recipes.append(new) if new < 10 else recipes.extend([1,new%10])
		elves = [(e + recipes[e] + 1) % len(recipes) for e in elves]
	return(p1,p2)

print(getrecipes(37, inp, 10))