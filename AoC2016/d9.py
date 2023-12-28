from aoc import *


def solve(input_str):
	p1, p2 = 0, 0
	i = 0
	while i < len(input_str):
		if input_str[i] == "(":
			last_i = i
			i += 1
			while input_str[i] != ")":
				i += 1
			a, b = map(int, input_str[last_i+1:i].split("x"))
			p1 += int(a)*int(b)
			p2 += b * solve(input_str[i+1:i+a+1])[1]
			i += a
		else:
			p2 += 1
			p1 += 1
		i += 1
	return p1, p2


setday(9)

data = parselines()[0]

print('part1: %s\npart2: %s' % solve(data))
