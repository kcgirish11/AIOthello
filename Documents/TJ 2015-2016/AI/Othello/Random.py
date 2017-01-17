import sys, random
import modmod

board = sys.argv[1]
char = sys.argv[2]

posSet = getPossMoves(board, char) 
findPossibleMove0(posSet)
def findPossibleMove0(posSet):
	return random.choice(list(posSet))
