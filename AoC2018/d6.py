inputHandle = open("d6.txt")
input = sorted(inputHandle.readlines())
inputHandle.close()

from collections import defaultdict

xMin = yMin = 2**31
xMax = yMax = 0

points = defaultdict(int)
for i in range(len(input)):
	x,y = input[i].split(", ")
	x,y = int(x), int(y)
	points[i] = x,y
	xMin = min(x, xMin)
	yMin = min(y, yMin)
	xMax = max(x, xMax)
	yMax = max(y, yMax)

for i in range(len(points)):
	points[i] = (points[i][0] - xMin, points[i][1] - yMin)

xMax -= xMin
yMax -= yMin
xMin, yMin = 0, 0

grid = [[0 for i in range(yMin,yMax)] for i in range(xMin,xMax)]

# gonna go full pajeet today (o(n^3), woo)
for x in range(xMin, xMax):
	for y in range(yMin, yMax):
		best = 1000
		bestID = -1
		for c in points:
			dist = abs(x - points[c][0]) + abs(y - points[c][1])
			
			if (dist < best):
				best = dist
				bestID = c
			elif (dist == best):
				best = dist
				bestID = -1
		grid[x][y] = bestID

# nuke any IDs touching the edge since they're probably infinite
badIDs = set()
for i in range(xMin,xMax):
	badIDs.add(grid[i][yMin])
	badIDs.add(grid[i][yMax-1])
for i in range(yMin,yMax):
	badIDs.add(grid[xMin][i])
	badIDs.add(grid[xMax-1][i])
	
for x in range(xMin,xMax):
	for y in range(yMin,yMax):
		if grid[x][y] in badIDs:
			grid[x][y] = -1

# tally areas
biggestID = defaultdict(int)
for x in range(xMin,xMax):
	for y in range(yMin,yMax):
		biggestID[grid[x][y]] += 1
del biggestID[-1]

print(max(biggestID.values()))

#p2
safeArea = 0
for x in range(xMin,xMax):
	for y in range(xMin,xMax):
		total = 0
		for c in points:
			total += abs(x - points[c][0]) + abs(y - points[c][1])
		if (total < 10000):
			safeArea += 1
print(safeArea)