import sys, random
#sys.stdout = open('test.txt', 'a')
board = sys.argv[1]
char = sys.argv[2]
neighDict = {}
def createDictionary():
	global neighDict 
	for pos in range(64): 
		neigh = set()
		if pos < 56: #bottom neighbors
			neigh.add(pos+8)
			if pos % 8 != 0: 
				neigh.add(pos+7)
			if (pos%8 !=7):
				neigh.add(pos+9)
		if pos >= 8:  #upper neighbors
			neigh.add(pos-8)
			if pos % 8 != 0: 
				neigh.add(pos-9)
			if pos % 8 != 7: 
				neigh.add(pos-7)
		if pos % 8 != 0:  #left
			neigh.add(pos-1)
		if pos % 8 != 7:  #right
			neigh.add(pos+1)
		neighDict[pos] = neigh 

def findPossibleMoves(char, board): 
	possSet = set()
	if char == "X": 
		for pos in range(len(board)): 
			if board[pos] == ".":
				for neigh in neighDict[pos]: 
					#print neigh
					if board[neigh] == "O": 
						diff = neigh - pos 
						nxt = neigh + diff
						while nxt in neighDict[neigh] and board[nxt] != ".": 
							if board[nxt] == "X": 
								possSet.add(pos)
								break
							neigh = nxt 
							nxt = neigh + diff
		return possSet
	elif char == "O":
		for pos in range(len(board)): 
			if board[pos] == ".":
				for neigh in neighDict[pos]: 
					if board[neigh] == "X": 
						diff = neigh - pos 
						nxt = neigh + diff
						while nxt in neighDict[neigh] and board[nxt] != ".": 
							if board[nxt] == "O": 
								possSet.add(pos)
								break
							neigh = nxt 
							nxt = neigh + diff
		return possSet
							

def findIndex2(posSet, playTurn): 
	pos2MinNextMoves = {}
	for pos in posSet: 
		if playTurn == "X": 
			fakeboard = board[:pos] + "X" + board[pos+1:]
			posOSet = findPossibleMoves("O", fakeboard)
			pos2MinNextMoves[pos] =  len(posOSet)
		else: 
			fakeboard = board[:pos] + "O" + board[pos+1:]
			posXSet = findPossibleMoves("X", fakeboard)
			pos2MinNextMoves[pos] =  len(posXSet)
	pos = random.choice(list(posSet))
	leng = pos2MinNextMoves[pos]
	for p in pos2MinNextMoves: 
		if pos2MinNextMoves[p] < leng: 
			leng = pos2MinNextMoves[p]
			pos = p
	return pos

createDictionary()
possibleMoves = findPossibleMoves(char, board)
print(findIndex2(possibleMoves, char))
