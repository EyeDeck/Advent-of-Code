inputHandle = open("d1.txt")
input = inputHandle.read()
inputHandle.close()

total = 0

adjustments = input.split("\n")
for e in adjustments:
	total += int(e)

print(total)