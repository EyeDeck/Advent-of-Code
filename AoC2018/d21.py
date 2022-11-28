inp = open("d21.txt").read()

import re
from collections import defaultdict

def mutate(reg, i, v):
	r = reg.copy()
	r[i] = v
	return r

#copied from d16
instructions = {
	"addr": lambda reg, op: mutate(reg, op[3], reg[op[1]] + reg[op[2]]),
	"addi": lambda reg, op: mutate(reg, op[3], reg[op[1]] + op[2]),
	
	"mulr": lambda reg, op: mutate(reg, op[3], reg[op[1]] * reg[op[2]]),
	"muli": lambda reg, op: mutate(reg, op[3], reg[op[1]] * op[2]),
	
	"banr": lambda reg, op: mutate(reg, op[3], reg[op[1]] & reg[op[2]]),
	"bani": lambda reg, op: mutate(reg, op[3], reg[op[1]] & op[2]),
	
	"borr": lambda reg, op: mutate(reg, op[3], reg[op[1]] | reg[op[2]]),
	"bori": lambda reg, op: mutate(reg, op[3], reg[op[1]] | op[2]),
	
	"setr": lambda reg, op: mutate(reg, op[3], reg[op[1]]),
	"seti": lambda reg, op: mutate(reg, op[3], op[1]),
	
	"gtir": lambda reg, op: mutate(reg, op[3], 1 if op[1] > reg[op[2]] else 0),
	"gtri": lambda reg, op: mutate(reg, op[3], 1 if reg[op[1]] > op[2] else 0),
	"gtrr": lambda reg, op: mutate(reg, op[3], 1 if reg[op[1]] > reg[op[2]] else 0),
	
	"eqir": lambda reg, op: mutate(reg, op[3], 1 if op[1] == reg[op[2]] else 0),
	"eqri": lambda reg, op: mutate(reg, op[3], 1 if reg[op[1]] == op[2] else 0),
	"eqrr": lambda reg, op: mutate(reg, op[3], 1 if reg[op[1]] == reg[op[2]] else 0),
}

prog = [tuple([i[0]] + [int(j) for j in i[1:]]) for i in re.compile("\n(\D+) (\d+) (\d+) (\d+)").findall(inp)]
ipreg = int(inp[4])

def process(p, reg, iters=-1):
	i = 0
	ip = 0
	seenregs = set()
	seenlist = []
	lastseen = 0
	#dbg = 0
	while i != iters:
		cins = p[ip]
		#print("pointer", ip, "	instruction", cins, "	register", reg)
		#if dbg == 0:
		#	inp = input()
		#	dbg -= int(inp) if inp else exit()
		if ip == 28:
			if reg[3] not in seenregs:
				seenregs.add(reg[3])
				lastseen = reg[3]
				# print(lastseen)
			else:
				#print(seenlist)
				print("Found the loop at ", reg[3], "; prior value was", lastseen)
				return(lastseen, i)
		reg[ipreg] = ip
		reg = instructions[cins[0]](reg, cins)
		ip = reg[ipreg]
		ip += 1
		if (ip > len(prog)-1):
			return(reg, i)
		i += 1
		
		#dbg = min(dbg+1,0)
	return(reg, i)

#bruteforce while I analyze
#for i in range(2000000,10000000):
#	reg, ins = process(prog, [i,0,0,0,0,0],2000)
#	if ins < 2000:
#		print(i, "returned in", ins, reg)
#	
#	if i % 100000 == 0:
#		print(i)

#turns out the answer was just sitting there in one of the registers,
#all I had to do was look at what was going on when the pointer was set to 28
p1, num = process(prog, [2792537,0,0,0,0,0])
print("P1:", p1, num)

# this is really slow but I can't be fucked to optimize this, fuck elfcode and fuck the elves
p2, num = process(prog, [1,0,0,0,0,0])
print("P2:", p2, num)