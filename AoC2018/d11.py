inp = 7315
gridsize = 300

import numpy as np

arr = np.zeros((gridsize,gridsize))
for x in range(gridsize):
	for y in range(gridsize):
		arr[x][y] = ((((x+11) * (y+1) + inp) * (x+11)) // 10**2 % 10) - 5

best = (0,0,0)
for x in range(1,gridsize-2):
	for y in range(1,gridsize-2):
		total = np.sum(arr[x:x+3,y:y+3])
		if (total > best[2]):
			best = (x+1,y+1,total)
print("best:", str(best[0])+","+str(best[1])+" (total: "+str(best[2])+")")

best = (0,0,0,0)
for s in range(1,300):
	for x in range(1,gridsize-s+1):
		for y in range(1,gridsize-s+1):
			total = np.sum(arr[x:x+s,y:y+s])
			if (total > best[2]):
				best = (x+1,y+1,total,s)
	print("\r"+str(s)+"/"+str(gridsize)+"... best:", str(best[0])+","+str(best[1])+","+str(best[3])+" (total: "+str(best[2])+")", end="")