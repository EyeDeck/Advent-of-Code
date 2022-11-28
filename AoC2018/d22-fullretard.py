#please don't look at my shame
#this file contains my many failed attempts at coming up with an algorithm to solve part 2

inp = open("d22.txt").read()

import re, numpy as np, collections

import heapq

disp = {0:".", 1:"=", 2:"|"}

def getcost(tile, tool, isgoal):
	# MAXIMUM OVERPAJEET
	# 0 = rocky, 1 = wet, 2 = narrow
	# 0 = torch, 1 = gear, 2 = either, 3 = torch/neither, 4 = gear/neither, 5 = neither
	
	# 0 = none, 1 = torch, 2 = gear ; 3 = torch/neither, 4 = gear/neither, 5 = either
	
	cost = 1
	if isgoal:
		if tool in [0, 2, 4]:
			cost += 7
			tool = 1
		elif tool in [3, 5]:
			tool = 1
		return cost, tool
	
	if tile == 0:
		if tool == 0:
			cost += 7
			tool = 5
		elif tool == 3:
			tool = 1
		elif tool == 4:
			tool = 2
	elif tile == 1:
		if tool == 1:
			cost += 7
			tool = 4
		elif tool == 3:
			tool = 0
		elif tool == 5:
			tool = 2
	else: # tile == 2
		if tool == 2:
			cost += 7
			tool = 3
		elif tool == 4:
			tool = 0
		elif tool == 5:
			tool = 1
	return cost, tool

class PriorityQueue:
	def __init__(self):
		self.elements = []
	
	def empty(self):
		return len(self.elements) == 0
	
	def put(self, item, priority):
		heapq.heappush(self.elements, (priority, item))
	
	def get(self):
		return heapq.heappop(self.elements)[1]

def heuristic(a, b):
	(x1, y1) = a
	(x2, y2) = b
	return abs(x1 - x2) + abs(y1 - y2)

def astar(graph,start,goal):
	dir = {"N":(0,-1), "S":(0,1), "E":(1,0), "W":(-1,0)}
	bounds = len(board)-1, len(board[0])-1
	
	frontier = PriorityQueue()
	frontier.put(start, 0)
	
	# this is a really really ugly hack, but I don't care at this point
	tools = {frozenset([(0,0)]):1}

	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0
	
	while not frontier.empty():
		current = frontier.get()
		
		path = set([current])
		cur = came_from[current]
		while cur != None:
			path.add(cur)
			cur = came_from[cur]
		path = frozenset(path)
#		print("path:", path, "\ntools:", tools)
		tool = tools[path] # tools.pop(path)
		# print(tools)
		#print(tool)
		
		if current == goal:
			break
		
		for d in dir.values():
			next = tuple(np.add(current, d))
			if next[0] < 0 or next[1] < 0 or next[0] > bounds[0] or next[1] > bounds[1]:
				continue
			
			thistile = board[next]
			thiscost, thistool = getcost(thistile, tool, next==goal)
			thiscost += cost_so_far[current]
			
			if next not in cost_so_far or thiscost < cost_so_far[next]:
				cost_so_far[next] = thiscost
				priority = thiscost + heuristic(goal, next)
				frontier.put(next, priority)
				came_from[next] = current
				# print( frozenset(path.union({next})) )

				tools[ frozenset(path.union({next})) ] = thistool
				
#				print(render(board, {next:"X"}, makeoverlay(path,"~")),
#				"current", current, "tool", thistool,
#				"; next", next, "is tile", thistile, "required tool", tool, "and cost", thiscost) #"took a tool switch" if thistool != tool else "took no switch")
#				input()
	
	return came_from, cost_so_far

def bfs(board,start,goal):
	dir = {"N":(0,-1,-1), "S":(0,1,-1), "E":(1,0,-1), "W":(-1,0,-1), "None":(0,0,0), "Torch":(0,0,1), "Gear":(0,0,2)}
	bounds = len(board)-1, len(board[0])-1
	
	seen = {start}
	
	stack = collections.deque([[start]])
	timestack = collections.deque([0])
	
	finished = []
	finishedtime = []
	while stack:
		path = stack.popleft()
		time = timestack.popleft()
		
		for d in dir.values():
			thistool = path[-1][2] if d[2] == -1 else d[2]
			#print(path[-1][2], thistool, d[2])
			
			this = (path[-1][0] + d[0], path[-1][1] + d[1], thistool)
			if this in seen or this[0] < 0 or this[1] < 0 or this[0] > bounds[0] or this[1] > bounds[1]:
				continue
			
			thistile = board[this[0], this[1]]
			if (thistile == thistool):
				continue
			
			thistime = time
			if path[-1][2] == thistool:
				thistime += 1
			else:
				thistime += 7
			
			if this == goal:
				while input("look!") == "":
					None
				finished.append(path + [this])
				finishedtime.append(thistime)
				continue
			
			seen.add(this)
			stack.append(path + [this])
			timestack.append(thistime)
			
			#print( render(board, mask=makeoverlay({x[0:2] for x in stack[-1]}, "~")) )
			#input()
	return finished

def makeoverlay(coords, char):
	return {c:char for c in coords}

def render(board, overlay={}, mask={}):
	tostr = []
	for y in range(len(board)):
		for x in range(len(board[y])):
			if (y, x) in overlay:
				tostr.append(overlay[(y,x)])
			elif mask and (y,x) not in mask:
				tostr.append(" ")
			else:
				tostr.append(disp[board[y][x]])
		tostr.append("\n")
	return "".join(tostr)

r = re.findall("depth: (\d+)\ntarget: (\d+),(\d+)", inp)
depth, target = int(r[0][0]), (int(r[0][1]),int(r[0][2]))
target = target[::-1]
target, depth = (10,10), 510
#target, depth = (30,30), 20

board = np.zeros((target[0]*10,target[1]*10), int)
# print(board, len(board), len(board[0]))

# faster for p1, but gotta use the dumb method for p2
#for x in range(1,len(board[0])):
#	board[0][x] = (x*16807 + depth) % 20183
#for y in range(1,len(board)):
#	board[y][0] = (y*48271 + depth) % 20183 
#for y in range(1,len(board)):
#	for x in range(1,len(board[y])):
#		board[y][x] = (board[y-1][x] * board[y][x-1] + depth) % 20183

for y in range(0,len(board)):
	for x in range(0,len(board[y])):
		if (y,x) == target:
			board[target] = 0 + depth
		elif y == 0:
			if x == 0:
				board[0][x] = 0 + depth
			else:
				board[0][x] = (x*16807 + depth) % 20183
		elif x == 0:
			board[y][0] = (y*48271 + depth) % 20183
		else:
			board[y][x] = (board[y-1][x] * board[y][x-1] + depth) % 20183
		#print("(",x,y,") is ",str(board[y][x]),"from",board[y-1][x], board[y][x-1])
		#print(render(board % 3))

board = board % 3
#print(render(board, {(0,0):"M", target:"T"}))

print(sum(sum(board[0:target[0]+1,0:target[1]+1])))

path, costs = astar(board, (0,0), target)
bestpath = set()
cur = path[target]
print(costs[target])
while cur != None:
	bestpath.add(cur)
	cur = path[cur]
print(render(board, makeoverlay(bestpath,"~")))
print(render(board, mask=makeoverlay(bestpath,"")))

#print(asr[0],"\n\n",asr[1])

#p2: 1031 too high