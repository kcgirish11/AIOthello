import sys
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

def flipRest(index, board): 
	flippedPieces = []
	flippedPieces.append(index)
	if board[index] == "X": 
		for neigh in neighDict[index]: 
			if board[neigh] == "O": 
				diff = neigh - index
				nxt = neigh + diff
				while nxt in neighDict[neigh] and board[nxt] != ".":
					if board[nxt] == "X":  
						while neigh != index: 
							board = board[:neigh] + "X" + board[neigh+1:]
							flippedPieces.append(neigh)
							neigh = neigh - diff
						break
					neigh = nxt 
					nxt = neigh + diff
	elif board[index] == "O": 
		for neigh in neighDict[index]: 
			if board[neigh] == "X": 
				diff = neigh - index
				nxt = neigh + diff
				while nxt in neighDict[neigh] and board[nxt] != ".": 
					if board[nxt] == "O": 
						while neigh != index: 
							board = board[:neigh] + "O" + board[neigh+1:]
							flippedPieces.append(neigh)
							neigh = neigh - diff
						break
					neigh = nxt 
					nxt = neigh + diff
	return board

def unflipRest(pos, flipped): 
	global board 
	if board[pos] == "X": playturn = "O"
	else: playturn = "X"
	for ind in flipped: 
		board = board[:ind] + playturn + board[ind+1:]
	board = board[:pos] + "." + board[:pos+1]


#Total # of human pieces - # of computer pieces							
def boardScore(): 
	#if we are X
	oCount = 0
	xCount = 0
	for pos in range(len(board)): 
		if board[pos] == "O":
			oCount += 1 
		elif board[pos] == "X": 
			xCount += 1
	if char == "X": 
		return xCount - oCount
	elif char == "O":
		return oCount - xCount

def maxValue(depth, playTurn, board, alpha, beta):
	tuplesofPosMoves = [] 
	if playTurn == "O": playTurn = "X"
	else: playTurn = "O" 
	for pos in findPossibleMoves(playTurn, board): 
		fakeboard = board[:pos] + playTurn + board[pos+1:]
		flipped = flipRest(pos, fakeboard)
		childValue = 0
		if depth == 0: 
			childValue = boardScore()
		elif depth != 0: 
			childValue = minValue(depth-1, playTurn, flipped, alpha, beta)
		tuplesofPosMoves.append(childValue)
		if childValue > alpha: 
			alpha = childValue
		if beta < alpha: 
			return childValue
	if tuplesofPosMoves: 
		return max(tuplesofPosMoves)
	elif depth == 0: 
		return boardScore()
	else: 
		return minValue(depth-1, playTurn, board, alpha, beta)
def minValue(depth, playTurn, board, alpha, beta):
	tuplesofPosMoves = [] 
	if playTurn == "X": playTurn = "O"
	else: playTurn = "X"
	for pos in findPossibleMoves(playTurn, board): 
		fakeboard = board[:pos] + playTurn + board[pos+1:]
		flipped = flipRest(pos, fakeboard) 
		childValue = 0
		if depth == 0: 
			childValue = boardScore()
		elif depth != 0: 
			childValue = maxValue(depth-1, playTurn, flipped, alpha, beta)
		tuplesofPosMoves.append(childValue)
		if childValue < beta: 
			beta = childValue
		if beta < alpha: 
			return childValue
	if tuplesofPosMoves: 
		return min(tuplesofPosMoves)
	elif depth == 0: 
		return boardScore()
	else: 
		return maxValue(depth-1, playTurn, board, alpha, beta)

createDictionary()
posSet = findPossibleMoves(char,board)
if len(posSet) == 1: 
	print (posSet.pop())
else:
	tuplesForreal = []
	alpha = float('-inf')
	beta = float('inf')
	for pos in posSet:
		fakeboard = board[:pos] + char + board[pos+1:]
		flipped = flipRest(pos, fakeboard) 
		value = maxValue(3, char, flipped, alpha, beta)
		tuplesForreal.append((value, pos))
	if tuplesForreal: 
		(val, posIwant) = min(tuplesForreal)
		print (posIwant)




				
