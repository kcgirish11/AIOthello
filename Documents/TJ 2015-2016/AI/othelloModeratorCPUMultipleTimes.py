
import sys, random

# string = ""
# for i in range((3*8)+3): 
# 	string = string + "."

# string = string + "X"
# string = string + "O"

# for i in range(6): 
# 	string = string + "."

# string = string + "O"
# string = string + "X"
# for i in range((3*8)+3): 
# 	string = string + "."

# #print string

global board 
board = ""
def startGame(): 
	global board
	board = "...........................XO......OX..........................."
	showBoard(board)

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
							
	else: 
		print "NOT A VALID CHARACTER"
def showBoard(board): 
	print "   ", 
	for l in range(8): 
		print "-",
	print
	for i in range(8): 
		print i,
		print "|",
		for k in range(8):  
			print board[i*8 + k], 
		print "|",
		print i
	print "   ", 
	for l in range(8): 
		print "-",
	print
	print "   ",
	for m in range(8): 
		print m,
	print

def flipRest(index): 
	global board
	if board[index] == "X": 
		for neigh in neighDict[index]: 
			if board[neigh] == "O": 
				diff = neigh - index
				nxt = neigh + diff
				while nxt in neighDict[neigh] and board[nxt] != ".":
					if board[nxt] == "X":  
						while neigh != index: 
							board = board[:neigh] + "X" + board[neigh+1:]
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
							neigh = neigh - diff
						break
					neigh = nxt 
					nxt = neigh + diff


def findIndex0(posSet): 
	return random.choice(list(posSet))

#corners
def findIndex1(posSet): 
	if 0 in posSet: 
		return 0 
	if 7 in posSet: 
		return 7
	if 56 in posSet: 
		return 56
	if 63 in posSet: 
		return 63
	else: 
		return random.choice(list(posSet))

def findIndex2(posSet, playTurn): 
	pos2MinNextMoves = {}
	leng2Pos = {}
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




def playNow(): 
	global board
	Alg1Count = 0 
	Alg2Count = 0
	Draw = 0
	numGames = int(sys.argv[1])
	for k in range(numGames*2):
		gameOver = False
		playTurn = "X" 
		board = "...........................XO......OX..........................."
		while not gameOver: 
		 	while playTurn == "X": 
				illegal = True
				while illegal:
					posXSet = findPossibleMoves(playTurn, board)
					posOSet = findPossibleMoves("O", board)
					if not posXSet and not posOSet: 
						gameOver = True
						break
					if not posXSet: 
						playTurn = "O"
						illegal = False
						break
					index = int()
					if k <= numGames: 
						index = findIndex2(posXSet, playTurn)
					else: 
						index = findIndex0(posXSet)
					board = board[:index] + "X" + board[index+1:]
					flipRest(index)
					#showBoard(board)
					playTurn = "O"
					illegal == False
					break
				break

			while playTurn == "O": 
				illegal = True
				while illegal:
					posOSet = findPossibleMoves(playTurn, board)
					posXSet = findPossibleMoves("X", board)
					if not posXSet and not posOSet: 
						gameOver = True
						break
					if not posOSet: 
						playTurn = "X"
						illegal = False
						break
					index = int()
					if k <= numGames: 
				 		index = findIndex0(posOSet)
				 	else: 
				 		index = findIndex2(posOSet, playTurn)
					board = board[:index] + "O" + board[index+1:]
					flipRest(index)
					#showBoard(board)
					playTurn = "X"
					illegal == False
					break
				break

		xcount = 0
		ocount = 0
		for char in board: 
			if char == "X": 
				xcount += 1
			if char == "O": 
				ocount += 1

		if xcount > ocount and k <= numGames: 
			Alg1Count += 1
			#print "XWINS"
		elif ocount > xcount and k <= numGames: 
			Alg2Count += 1
			#print "OWINS"
		elif k > numGames and ocount >xcount: 
			Alg1Count += 1
			#print "OWINS"
		elif k > numGames and xcount >ocount: 
			Alg2Count += 1
			#print "XWINS"
		elif xcount == ocount: 
			Draw += 1 
	print "Algorithim 1 Wins " + str(Alg1Count)
	print "Algorithim 2 Wins " + str(Alg2Count)
	print "Draws " + str(Draw)


#startGame()
createDictionary()
playNow()