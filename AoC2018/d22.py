inp = open("d22.txt").read()

import re, numpy as np, collections, heapq

def makeoverlay(coords, char):
	return {c:char for c in coords}

def render(board, overlay={}, mask={}):
	disp = {0:".", 1:"=", 2:"|"}
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
	(x1, y1) = a[0], a[1]
	(x2, y2) = b[0], b[1]
	return abs(x1 - x2) + abs(y1 - y2)

#behold, the defiled corpse of an a* algorithm (most of this code was lifted straight from google)
def astar(graph, start, goal):
	dir = {"N":(0,-1,-1), "S":(0,1,-1), "E":(1,0,-1), "W":(-1,0,-1), "None":(0,0,0), "Torch":(0,0,1), "Gear":(0,0,2)}
	bounds = len(board)-1, len(board[0])-1
	
	frontier = PriorityQueue()
	frontier.put(start, 0)
	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0
	
	while not frontier.empty():
		current = frontier.get()
		
		if current == goal:
			break
		
		for d in dir.values():
			thistool = current[2] if d[2] == -1 else d[2]
			
			next = (current[0] + d[0], current[1] + d[1], thistool)
			if next[0] < 0 or next[1] < 0 or next[0] > bounds[0] or next[1] > bounds[1]:
				continue
			
			thistile = board[next[0], next[1]]
			if (thistile == thistool):
				continue
			
			thiscost = cost_so_far[current]
			if current[2] == thistool:
				thiscost += 1
			else:
				thiscost += 7
			
			if next not in cost_so_far or thiscost < cost_so_far[next]:
				cost_so_far[next] = thiscost
				priority = thiscost + heuristic(goal, next)
				frontier.put(next, priority)
				came_from[next] = current
	
	return came_from, cost_so_far

r = re.findall("depth: (\d+)\ntarget: (\d+),(\d+)", inp)
depth, target = int(r[0][0]), (int(r[0][1]),int(r[0][2]))
target = target[::-1]
#target, depth = (10,10), 510

board = np.zeros((target[0]+30,target[1]*5), int)

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

board = board % 3
#print(render(board, {(0,0):"M", target:"T"}))

print("P1:", sum(sum(board[0:target[0]+1,0:target[1]+1])))

aspath, ascost = astar(board, (0,0,1), (target[0], target[1], 1))
print("P2:", ascost[(target[0], target[1], 1)])