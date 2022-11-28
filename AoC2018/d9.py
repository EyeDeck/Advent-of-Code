inp = "432 players; last marble is worth 71019 points"
parsed = inp.split()

from blist import blist

def p1(playerct, lastmarble):
	currentplayer = 1
	currentmarble = 0
	players = [0]*playerct
	board = blist([0])
	marbles = [i for i in range(lastmarble+1, 0, -1)]

	while (marbles):
		if (marbles[-1] % 23 == 0):
			currentmarble -= 7
			if (currentmarble > len(board)):
				currentmarble -= len(board)
			if (currentmarble < 0):
				currentmarble += len(board)
			
			players[currentplayer] += marbles.pop() + board.pop(currentmarble)
		else:
			currentmarble += 2
			f = 0
			if (currentmarble > len(board)):
				f = currentmarble
				currentmarble -= len(board)
			if (currentmarble < 0):
				f = currentmarble
				currentmarble += len(board)
			
			board.insert(currentmarble, marbles.pop())
		
		currentplayer += 1
		if (currentplayer == playerct):
			currentplayer = 0
		
	return(max(players))

print(p1(int(parsed[0]), int(parsed[6])))
print(p1(int(parsed[0]), int(parsed[6])*100))

#testlist = [[10, 1618, 8317], [13, 7999, 146373], [17, 1104, 2764], [21, 6111, 54718], [30, 5807, 37305]]
#for test in testlist:
#	print("Got",p1(test[0],test[1]),", should be",test[2])
