inp = open("d16.txt").read()

import re
# import operator
from collections import defaultdict

cases = [([int(i) for i in case[0].split(",")], [int(i) for i in case[1].split()], [int(i) for i in case[2].split(",")]) for case in re.compile("Before: \[(\d+, \d+, \d+, \d+)\]\n(\d+ \d+ \d+ \d+)\nAfter:  \[(\d+, \d+, \d+, \d+)\]").findall(inp)]
testprog = [[int(i) for i in line.split()] for line in re.compile("(\d+ \d+ \d+ \d+)").findall(inp)[len(cases):]]

#print(cases)
#print(something)

#def addr(reg, op):
#	reg[op[3]] = 
#	return (reg)

def mutate(reg, i, v):
	r = reg.copy()
	r[i] = v
	return r

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

insmap = {}

# print(operators["addr"]([3, 2, 1, 1], [9, 2, 1, 2]))

p1 = 0
for case in cases:
	ct = 0
	for name,ins in instructions.items():
		if ins(case[0], case[1]) == case[2]:
			ct += 1
	if ct >= 3:
		p1 += 1
print("Part1:", p1)

bins = {i:[] for i in range(16)}
for case in cases:
	bins[case[1][0]].append(case)

#naive bruteforce woo
unfound = {i for i in instructions.keys()}
while True:
	poss = {}
	for id,bin in bins.items():
		for name,ins in instructions.items():
			if name not in unfound:
				continue
			passes = True
			for case in bin:
				if ins(case[0], case[1]) != case[2]:
					passes = False
					continue
			if passes:
				# print("All cases in bin ID", id, "seem to pass check for instruction", name)
				if id not in poss:
					poss[id] = []
				poss[id].append(name)
				continue
	if not poss:
		break
	for k,v in poss.items():
		if len(v) == 1:
			del bins[k]
			unfound.remove(v[0])
			insmap[k] = v[0]

#print(sorted(insmap.items()))

reg = [0,0,0,0]
for ins in testprog:
	#newreg = instructions[insmap[ins[0]]](reg, ins)
	#print("performing",ins,"using instruction",insmap[ins[0]],"on",reg,"=",newreg)
	reg = instructions[insmap[ins[0]]](reg, ins)
print(reg)