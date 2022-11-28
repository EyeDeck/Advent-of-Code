inp = open("d23.txt").readlines()

import re
from operator import itemgetter
from z3 import *

def dist(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def checkaround(tocheck, start, d, res, fromzero=False):
	best = (0,0,0)
	bestct = 0
	bestz = 0x7FFFFFFF
	for x in range(start[0]-d,start[0]+d,res):
		#if fromzero:
		#	print(x)
		for y in range(start[1]-d,start[1]+d,res):
			for z in range(start[2]-d,start[2]+d,res):
				thisct = 0
				thisz = 0
				for bot in tocheck:
					if dist((x,y,z), (bot[0], bot[1], bot[2])) <= bot[3]:
						thisct += 1
				if fromzero:
					thisz = sum((x,y,z))
				if (thisct > bestct or fromzero and thisct == bestct and thisz < bestz):
					best = (x,y,z)
					bestct = thisct
					bestz = thisz
					# print(bestct)
	return best, bestct

exp = re.compile("[-\d]+")
parsed = [[int(i) for i in exp.findall(l)] for l in inp]

strongestbot = max(parsed, key=itemgetter(3))
botct = 0
for bot in parsed:
	if dist((bot[0], bot[1], bot[2]), (strongestbot[0], strongestbot[1], strongestbot[2])) <= strongestbot[3]:
		botct += 1
print("P1:", botct)

#bound = 0
#for bot in parsed:
#	bound = max(0, dist((bot[0], bot[1], bot[2]), (0,0,0)) - bot[3], bound)

## I think this could work if I figured out how to tune it better
#res = 0x170000
#bound = 0x8000000
#curbest = (0,0,0)
##res = 64
##bound = 1024
##curbest = (20664188, 23083996, 37752188)
#while True:
#	curbest, curct = checkaround(parsed, curbest, bound, res)
#	
#	if (bound <= 128):
#		bound //= 2
#		res //= 2
#	else:
#		bound //= 32
#		res //= 8
#	res = max(1,res)
#	
#	print(curbest, curct, ";", bound, res)
#	if bound == 0:
#		print(dist(curbest, (0,0,0)))
#		break

# 81500252 too low

#divisor = 1000000
#bound = 100000000
#res = 4
#curbest = (0,0,0)
#curct = 0
#loops = 0
#while True:
#	rcomplex = [[i//divisor for i in bot] for bot in parsed]
#	
#	curbest, curct = checkaround(rcomplex, curbest, 100, res, True)
#	print(curbest, curct, ";", bound, res)
#	divisor //= 10
#	if divisor == 0:
#		print(dist(curbest, (0,0,0)))
#		break
#	loops += 1
#	curbest = (curbest[0]*10, curbest[1]*10, curbest[2]*10)
## coords should be close, now narrow them down
#maybe_ans, maybe_ct= checkaround(parsed, curbest, 100, 1, True)
#print(maybe_ans, maybe_ct, sum(maybe_ans))

#print(checkaround(parsed, curbest, 1, 1))
#
#divisor = 1000
#res = 1
#curbest = [i//divisor for i in curpoint]
#curct = 0
#while True:
#	rcomplex = [[i//divisor for i in bot] for bot in parsed]
#
#	curbest, curct = checkaround(rcomplex, curbest, 1, 1)
#	print(curbest, curct, ";", res)
#	divisor //= 10
#	if divisor == 0:
#		print(dist(curbest, (0,0,0)))
#		break
#	
#	curbest = [i*10 for i in curbest]
## coords should be close, now narrow them down
#maybe_ans, maybe_ct= checkaround(parsed, curbest, 100, 1, True)
#print(maybe_ans, maybe_ct, sum(maybe_ans))

###trying an algo someone described on /g/
#def find_outside_radius(bots, start):
#	outside = []
#	for bot in bots:
#		if dist(bot, start) > bot[3]:
#			outside.append(bot)
#	return outside
#
#outside = parsed
#curpoint = [0,0,0]
#maxlen = len(parsed)
#lastlen = maxlen + 1
#while True:
#	thissum = [0,0,0]
#	for b in outside:
#		thissum = [b[0] + thissum[0], b[1] + thissum[1], b[2] + thissum[2]]
#	thissum = [i//len(outside) for i in thissum]
#	curpoint = thissum
#	outside = find_outside_radius(parsed, curpoint)
#	print(len(outside), maxlen)
#	thislen = maxlen - len(outside)
#	if lastlen == thislen:
#		break
#	input()
#	lastlen = thislen
#print(len(find_outside_radius(parsed, curpoint)))
#print("P2:", sum(curpoint))
##didn't work at all lol

# So if I had gotten a luckier input, my first couple of attempts at a solution
# would actually have worked, irritatingly, and I would have actually gotten on the 
# leaderboard for p2. I did not get lucky, however, so I had to go figure out how
# the fuck z3 works and use that instead since that seems to be the only solution
# that anyone has ever come up with for this fucking problem that consistently gives
# the correct answer for any input. Oh well, I got brainlet filtered on p2 yesterday
# anyway when I had to go find a hint on how to do the pathfinding.
# Just fuck my shit up senpai
def z3_abs(n):
	return If(n >= 0,n,-n)

def z3_dist(a, b):
	return z3_abs(a[0] - b[0]) + z3_abs(a[1] - b[1]) + z3_abs(a[2] - b[2])

x, y, z = Int("x"), Int("y"), Int("z")
tuplized = [((tuple(b[0:-1]), b[3])) for b in parsed]

orig = (x, y, z)
cost_expr = x * 0
for pos, range in tuplized:
	cost_expr += If(z3_dist(orig, pos) <= range, 1, 0)
opt = Optimize()
opt.maximize(cost_expr)
# opt.minimize(z3_dist((0,0,0), (x, y, z)))

opt.check()

model = opt.model()
best = (model[x].as_long(), model[y].as_long(), model[z].as_long())
# print(best)

print("P2:", best, "len", dist((0,0,0), best) )