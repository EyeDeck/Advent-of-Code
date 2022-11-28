inp = open("d19.txt").read()

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
	while i != iters:
		cins = p[ip]
		reg[ipreg] = ip
		reg = instructions[cins[0]](reg, cins)
		ip = reg[ipreg]
		ip += 1
		if (ip > len(prog)-1):
			return(reg)
		i += 1
	return(reg)

#naive soluton:
#p1 = process(prog, [0,0,0,0,0,0])
#print("P1:", p1[0], "(" + str(p1) + ")")

#p2 = process(prog, [1,0,0,0,0,0])
#print("P2:", p2[0], "(" + str(p2) + ")")

# I ended up figuring out p2 by looking at the registers until I noticed a pattern, then 
# used using fucking wolfram alpha to solve the rest
# what the input program does does is run the first 9 instructions for p1 and 17 for p2, 
# which sets register 5 to a number, then starts running the world's shittiest algoritmh 
# for finding the sum of that number's factors + itself

# here's the "correct" solution anyway, determined programatically

#shitty unoptimized function (fuck it)
def findfactors(num):
	factors = set([num])
	for i in range(1,num,2):
		if num % i == 0:
			factors.add(i)
	return(factors)

p1 = sum(findfactors(max(process(prog, [0,0,0,0,0,0], 9))))
print("P1:", p1)

p2 = sum(findfactors(max(process(prog, [1,0,0,0,0,0], 17))))
print("P2:", p2)

# I swear I came so fucking close to getting brainlet filtered on this one, took me 3 hours in the end