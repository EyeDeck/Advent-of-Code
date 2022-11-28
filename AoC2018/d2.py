inputHandle = open("d2.txt")
input = inputHandle.readlines()
inputHandle.close()

def p1():
	l2, l3 = 0, 0
	for box in input:
		chars = {}
		incl2, incl3 = False, False
		
		for c in box:
			if c in chars:
				chars[c] += 1
			else:
				chars[c] = 1
		
		for k,v in chars.items():
			if v == 2:
				incl2 = True
			elif v == 3:
				incl3 = True
				
		l2 += incl2
		l3 += incl3
		
	return(l2 * l3)
	
def p2():
	# naive solution
	seen = []
	for box in input:
		for box2 in seen:
			diff = 0
			for i in range(len(box)):
				if box[i] != box2[i]:
					diff += 1
					if diff > 1:
						break
			
			if diff == 1:
				output = ""
				for i in range(len(box) - 1):
					if box[i] == box2[i]:
						output += box[i]
				return(output)
		
		seen.append(box)

print(p1())
print(p2())