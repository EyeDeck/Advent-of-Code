import copy

# parsed by hand because I can't be fucked to do it programatically
# slashing = 0, bludgeoning = 1, fire = 2, cold = 3, radiation = 4
# ID: ID, army, unit count, hp, weaknesses, immunities, att dam, att type, initiative
units = {
	0:	[0,		0, 504, 	1697, 	[2],	[0],		28,		2,	4],
	1:	[1,		0, 7779,	6919, 	[1],	[],			7,		3,	2],
	2:	[2,		0, 7193,	13214,	[3, 2],	[],			12,		0,	14],
	3:	[3,		0, 1898,	3721, 	[1],	[],			16,		3,	20],
	4:	[4,		0, 843, 	3657, 	[],		[0],		41,		3,	17],
	5:	[5,		0, 8433,	3737, 	[1],	[4],		3,		1,	8],
	6:	[6,		0, 416, 	3760, 	[],		[2, 4],		64,		4,	3],
	7:	[7,		0, 5654,	1858, 	[2],	[],			2,		3,	6],
	8:	[8,		0, 2050,	8329, 	[],		[4, 3],		36,		4,	12],
	9:	[9,		0, 4130,	3560, 	[],		[],			8,		1,	13],
	10:	[10,	1, 442, 	35928,	[],		[],			149,	1,	11],
	11:	[11,	1, 61,  	42443,	[],		[4],		1289,	0,	7],
	12:	[12,	1, 833, 	6874, 	[0],	[],			14,		1,	15],
	13:	[13,	1, 1832,	61645,	[],		[],			49,		2,	9],
	14:	[14,	1, 487, 	26212,	[2],	[],			107,	1,	16],
	15:	[15,	1, 2537,	18290,	[],		[3, 0, 2],	11,		2,	19],
	16:	[16,	1, 141, 	14369,	[],		[1],		178,	4,	5],
	17:	[17,	1, 3570,	34371,	[],		[],			18,		4,	10],
	18:	[18,	1, 5513,	60180,	[4, 2],	[],			16,		0,	1],
	19:	[19,	1, 2378,	20731,	[1],	[],			17,		4,	18]
}

#units = {
#	0:	[0,		0, 17,		5390,	[4, 1],	[],			4507,	2,	2],
#	1:	[1,		0, 989,		1274,	[1, 0],	[2],		25,		0,	3],
#	2:	[2,		1, 801,		4706,	[4],	[],			116,	1,	1],
#	3:	[3,		1, 4485,	2961,	[2, 3],	[4],		12,		0,	4]
#}

boost = 0
def runsim(lunits):
	rounds = 0
	while True:
		# target selection:
		unitlist = sorted(lunits.values(), key=lambda x: (x[2]*x[-3], x[-1]), reverse=True)
		#dp = []
		#for u in unitlist:
		#	for u2 in unitlist:
		#		if u[0] == u2[0]:
		#			continue
		#		if u[2]*u[-3] == u2[2]*u2[-3]:
		#			dp.append((u, u2)) if (u2, u) not in dp else None
		#if dp:
		#	print(dp,"\n", unitlist)
		#	input()
		
		targets = []
		invalidtargets = set()
		
		for u in unitlist:
			besttargets = []
			bestdam = -1
			basedam = u[2]*u[-3]
		#	print(basedam)
			for t in unitlist:
				thisdam = basedam
				if u[1] == t[1] or t[0] in invalidtargets:
					continue
				
				if u[-2] in t[4]:
					thisdam *= 2
				if u[-2] in t[5]:
					thisdam = 0
				
				if thisdam == 0:
					continue
		#		print(thisdam,"vs",t)
				if thisdam > bestdam:
					besttargets = []
					bestdam = thisdam
				if thisdam >= bestdam:
					besttargets.append((u[0], t[0]))
			
			if not besttargets:
				continue
			
			besttargets = sorted(besttargets, key=lambda x: (lunits[x[1]][2]*lunits[x[1]][-3], lunits[x[1]][-1]), reverse=True)
			
			targets.append(besttargets[0])
			invalidtargets.add(besttargets[0][1])
		#	input()
			
		# target selection over
		if not targets:
			lunitsleft = 0
			for u in lunits.values():
				lunitsleft += u[2]
			winner = list(lunits.values())[0][1]
		#	if winner == 0:
		#		print(rounds, lunits)
			return (lunitsleft, winner)
		
		targets = sorted(targets, key=lambda x: lunits[x[0]][-1], reverse=True)
		
		stalemate = True
		for a in targets:
			if lunits[a[0]][2] <= 0:
				continue
			thisdam = lunits[a[0]][2]*lunits[a[0]][-3]
			if lunits[a[0]][-2] in lunits[a[1]][4]:
				thisdam *= 2
			tokill = thisdam//lunits[a[1]][3]
			#print(a[0], "deals", thisdam, "to", a[1], "killing", tokill)
			if tokill:
				stalemate = False
				lunits[a[1]][2] -= tokill
		
		if stalemate:
			return (-1,-1)
		
		lunits = {id:u for id,u in lunits.items() if u[2] > 0}
		
		#print(lunits)
		rounds += 1

print("P1:", runsim(copy.deepcopy(units)))

boost = 0
while True:
	boost += 1
	for id,u in units.items():
		if u[1] == 0:
			units[id][-3] += 1
	results = runsim(copy.deepcopy(units))
	if results[1] == 0:
		print("P2:", results, boost)
		break
