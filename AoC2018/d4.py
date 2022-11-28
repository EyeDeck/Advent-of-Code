# just kill me now
inputHandle = open("d4-bb.txt")
input = sorted(inputHandle.readlines())
inputHandle.close()
input.append("[1519-01-01 00:01] Guard #0 begins shift") # hack to ensure the last guard gets written during parsing without extra processing

import re

guards = {}
currentGuard = 0
currentSchedule = [0] * 60 # bytearray(60) works too
lastSleep = 0

parse = re.compile("\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.*)")
num = re.compile("(\d+)")

# parse schedules into byte arrays, stored per guard
for action in input:
	y,m,d,h,m,a = parse.findall(action)[0]
	#print(a)
	
	if (a.startswith("Guard")):
		if currentGuard not in guards:
			guards[currentGuard] = []
		guards[currentGuard].append(currentSchedule)
		
		currentGuard = int(num.search(a)[0])
		currentSchedule = [0] * 60
	elif (a == "falls asleep"):
		lastSleep = int(m)
	elif (a == "wakes up"):
		for i in range(lastSleep, int(m)):
			currentSchedule[i] = 1
guards.pop(0)

# sum guard schedules per guard
guardFreqs = {}
for k,_ in guards.items():
	if k not in guardFreqs:
		guardFreqs[k] = [0] * 60
		
	# print(str(k) + " " + str(guards[k]))
	for i in range(0, len(guards[k])):
		for j in range(0, len(guards[k][i])):
			# print(str(guardFreqs[k][i]) + " + " + str(guards[k][i][j]))
			guardFreqs[k][j] += guards[k][i][j]

# sum minutes of each guard's schedule
guardMinutes = {}
for k,v in guardFreqs.items():
	if k not in guardMinutes:
		guardMinutes[k] = 0
	
	for m in v:
		guardMinutes[k] += m

# find guard with most total minutes slept
sleepiestGuard = 0
mostMinutesSlept = 0
for k,v in guardMinutes.items():
	if v > mostMinutesSlept:
		sleepiestGuard = k
		mostMinutesSlept = v
# print(str(sleepiestGuard) + " slept " + str(mostMinutesSlept))

# find sleepist minute of said guard
sleepiestMinute = 0
mostMinutesSlept = 0
sl = guardFreqs[sleepiestGuard]
for i in range(0, len(sl)):
	if sl[i] > mostMinutesSlept:
		sleepiestMinute = i
		mostMinutesSlept = sl[i]

# jesus christ I can't believe how convoluted I wrote this to be
print("P1: " + str(sleepiestMinute * sleepiestGuard))

# at least I had the data structures parsed well enough to make p2 trivial
sleepiestGuard = 0
sleepiestMinute = 0
mostMinutesSlept = 0
for k,v in guardFreqs.items():
	for i in range(0, 60):
		if v[i] > mostMinutesSlept:
			sleepiestMinute = i
			sleepiestGuard = k
			mostMinutesSlept = v[i]
			# print(str(sleepiestMinute) + " " + str(sleepiestGuard) + " " + str(mostMinutesSlept))

print("P2: " + str(sleepiestMinute * sleepiestGuard))
