inputHandle = open("d1.txt")
input = inputHandle.readlines()
inputHandle.close()

total = 0

for e in input:
	total += int(e)
print("total: " + str(total))

total = 0
past = {0}
while True:
	for e in input:
		total += int(e)
		if (total in past):
			print("dupe: " + str(total))
			exit()
		past.add(total)