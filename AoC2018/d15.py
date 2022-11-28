inp = open("d15.txt").readlines()

import numpy as np
import operator
from collections import deque

class Combatant:
	def __init__(self, type, dam, hp):
		self.type = type
		self.dam = dam
		self.hp = hp

def parseboard(inp,stats):
	combatants = {}
	board = np.array([c for c in [list(l.rstrip("\n")) for l in inp]])
	board = np.rot90(np.flipud(board),3) # so I can access it as [x][y] and don't need to remember stupid coord systems
	# print("Printing",board)
	
	for x in range(len(board)):
		for y in range(len(board[x])):
			c = board[x][y]
			if c in stats:
				combatants[x,y] = Combatant(c, stats[c][0], stats[c][1])
				board[x][y] = "."
	
	return board, combatants

def step(board,combatants,p2=False):
	for cs, co in sorted(sorted(combatants.items()), key=lambda y: y[0][1]):
		if co not in combatants.values():
			continue
		
		#print("Attacker:", co.type, "at", cs)
		
		attacked = False
		for o in ro:
			this = getsq(board,combatants,tuple(map(operator.add, cs, o)),True)
			if isinstance(this, Combatant) and this.type != co.type:
				if attack(board,combatants,cs,co) and p2:
					return(True, False)
				attacked = True
				break
		if attacked:
			continue
		
		targets={(k,v) for k,v in combatants.items() if v.type != co.type}
		if len(targets) == 0:
			return(True, True) # combat ended
		
		inrange = set()
		# print([[t[0],t[1].type] for t in targets])
		for t in targets:
			for o in ro:
				this = tuple(map(operator.add, t[0], o))
				if getsq(board,combatants,this) == ".":
					inrange.add(this)
		#print("Valid target coords:")
		#print(render(board,combatants,makeoverlay(inrange,"?")))
		
		path = bfs(board, combatants, cs, inrange)
		
		if path:
			#print("Found target:")
			#print(render(board,combatants,{cs:"A",path[-1]:"+", **{x:"*" for x in path[1:-1]}}))
			combatants[path[1]] = combatants.pop(cs)
			
			if attack(board,combatants,path[1],co) and p2:
				return(True, False)
	
	return(False,False)

def attack(board,combatants,cs,co):
	#targets = [t for t in [getsq(board,combatants,tuple(map(operator.add, cs, o)),True) for o in ro] if isinstance(t, Combatant) and t.type != co.type]
	targets = []
	for o in ro:
		this = tuple(map(operator.add, cs, o))
		tile = getsq(board,combatants,this,True)
		if isinstance(tile, Combatant) and tile.type != co.type:
			targets.append((this, tile))
	if not targets:
		return(False)
	else:
		lowest = 0x7fffffff
		target = None
		for t in targets:
			if t[1].hp < lowest:
				lowest = t[1].hp
				target = t
		target[1].hp -= co.dam
		#print(co.type, "at", cs, "hits", target[1].type, "at", target[0], "for", co.dam, "damage—", target[1].hp, "hp remains.")
		if target[1].hp <= 0:
			#print(target[1].type, "at", target[0], "dies!")
			del combatants[target[0]]
			if (target[1].type == "E"):
				return(True)
	return(False)
	#print(cs,targets)
	#input()

def bfs(board,combatants,start,goals):
	visited = {start}
	current = deque([[start]])
	paths = []
	while current:
		path = current.popleft()
		x,y = path[-1]
		if paths and len(path) > len(paths[0]):
			break
		if (x,y) in goals:
			paths.append(path)
		for o in ro:
			this = tuple(map(operator.add, path[-1], o))
			if getsq(board,combatants,this) == ".":
				if this not in visited:
					current.append(path + [this])
					visited.add(this)
		#print(render(board,combatants,{**makeoverlay(visited,"-"), **makeoverlay(path,"~")}))
		#input()
	if paths:
		# have fun untangling this shit future me, you asshole
		dest = sorted(paths, key=lambda y: y[-1][1])[0][-1]
		return(sorted([i for i in paths if i[-1] == dest], key=lambda x: x[1][-1])[0])
	else:
		return None

def getsq(board,combatants,coords,obj=False):
	x,y = coords
	if (x,y) in combatants:
		if obj:
			return combatants[x,y]
		else:
			return combatants[x,y].type
	else:
		return board[x][y]

def makeoverlay(coords, char):
	return {c:char for c in coords}

def render(board,combatants,overlay={}):
	tostr = []
	for y in range(len(board[0])):
		for x in range(len(board)):
			if (x,y) in overlay:
				tostr.append(overlay[(x,y)])
			else:
				tostr.append(getsq(board,combatants,(x,y)))
			tostr.append(" ")
		tostr.append("\n")
	return "".join(tostr)

def runinput(inp, p2=False, prints=False):
	if p2:
		for i in range(3, 0xfff):
			stats = {"G":(3,200), "E":(i,200)}
			board, combatants = parseboard(inp, stats)
			ans = 0
			
			for j in range(0xfff):
				if prints:
					print("Round", j, "ends.", "\n"+render(board,combatants))
				outcome = step(board,combatants,True)
				if outcome == (True, True):
					print("Tried",i,", no elves died on round",j,"\n" + render(board,combatants) if prints else "")
					ans = sum([v.hp for c,v in combatants.items()]) * j
					return(ans)
				elif outcome == (True, False):
					if prints:
						print("Tried",i,",elf died on round",j,"\n",render(board,combatants))
					break
			if prints:
				print(render(board,combatants))
	else:
		stats = {"G":(3,200), "E":(3,200)}
		board, combatants = parseboard(inp, stats)
		ans = 0
		
		for i in range(0xfff):
			if prints:
				print("Round", i, "ends.")
				print(render(board,combatants))
			if step(board,combatants) == (True,True):
				ans = sum([v.hp for c,v in combatants.items()]) * i
				break
		if prints:
			print(render(board,combatants))
		return(ans)

ro = [(0,-1),(-1,0),(1,0),(0,1)] # reading order

#tests = [("d15-e5.txt", 36334), ("d15-e6.txt", 39514), ("d15-e7.txt", 27755), ("d15-e8.txt", 28944), ("d15-e9.txt", 18740), ("d15-e10.txt", 183300), ("d15-e11.txt", 207542)]

#for t in tests:
#	ans = runinput(open(t[0]).readlines())
#	if ans == t[1]:
#		print(t[0], "passed.")
#	else:
#		print(t[0], "failed—got", str(ans) + ", expected:" , t[1])

print("P1:", runinput(inp, False))
print("P2:", runinput(inp, True))

