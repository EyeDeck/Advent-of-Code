base = [int(i)//3-2 for i in open("d1.txt").readlines()]
p1 = sum(base)
print('p1:', p1)

p2 = 0
for v in base:
	while v >= 0:
		p2 += v
		v = v//3-2

print('p2:', p2)
