inputHandle = open("d5.txt")
input = inputHandle.read()
inputHandle.close()

import string

# slow-ass pajeet solution (gross)
def p1(inputList):
	lastChar = ""
	while True:
		didSomething = False
		for i in range(len(inputList)-1,0,-1):
			if (inputList[i] == lastChar.swapcase()):
				inputList.pop(i)
				inputList.pop(i)
				didSomething = True
				lastChar = ""
			else:
				lastChar = inputList[i]
		if (didSomething == False):
			return len(inputList)

# much better (like 150x faster lol)
def p1i(l):
	stack = []
	for c in l:
		if (len(stack) == 0):
			stack.append(c)
		else:
			tmp = stack.pop()
			if (tmp != c.swapcase()):
				stack.append(tmp)
				stack.append(c)
	return len(stack)

def p2():
	letters = list(string.ascii_lowercase)
	lowest = len(input)
	for i in range(0,len(letters)):
		this = p1i(input.replace(letters[i], "").replace(letters[i].swapcase(), ""))
		if (this < lowest):
			lowest = this
			print(str(lowest) + "... (" + letters[i] + ")", "")
	return lowest

# print(p1(list(input)))
print(p1i(input))
print(p2())