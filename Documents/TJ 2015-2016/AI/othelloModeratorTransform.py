
import sys, random

string = ""
for i in range((3*8)+3): 
	string = string + "."

string = string + "X"
string = string + "O"

for i in range(6): 
	string = string + "."

string = string + "O"
string = string + "X"
for i in range((3*8)+3): 
	string = string + "."

print string

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

#self
def self():
	return range(64)

#rotateLeft 
def rotateLeft(): 
	rlList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrow = col 
			newcol = 7 - row 
			rlList[index] = (8*newrow) + newcol 
	#print rlList
	return rlList

#rotateRight 
def rotateRight(): 
	rrList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrow = 7 - col 
			newcol = row 
			rrList[index] = (8*newrow) + newcol
	return rrList 

#rotate 180
def rotate180(): 
	r180List = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrow = col 
			newcol = 7 - row 
			newrrow = newcol 
			newccol = 7 - newrow
			r180List[index] = (8*newrrow) + newccol 
	return r180List

#flipX 
def flipX(): 
	xList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrrow = 7-row 
			xList[index] = (8*newrrow) + col 
	return xList 

#flipY
def flipY(): 
	yList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newcol = 7-col 
			yList[index] = (8*row) + newcol
	return yList

 
#flip diagnol y = x
def flipDiagnol(): 
	diagList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrow = 7 - col
			newcol = 7 - row
			diagList[index] = (8*newrow) + newcol
	return diagList

#flip zero y = -x
def flipZero(): 
	diagList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 	
			if row == col: 
				diagList[index] = index 
			else: 
				diagList[index] = (8*col) + row 
	return diagList



#build dictionary 
def buildTransform(): 
	transformDict = {}
	transformDict['i'] = self()
	transformDict['rl'] = rotateLeft()
	transformDict['rr'] = rotateRight()
	transformDict['r2'] = rotate180()
	transformDict['fx'] = flipX()
	transformDict['fy'] = flipY()
	transformDict['fo'] = flipZero() 
	transformDict['fd'] = flipDiagnol()
	return transformDict


dictTransform = buildTransform()

def transform(technique, puzzle): 
	newindex = dictTransform[technique]
	newboard = ""
	for ind in range(64): 
		newboard = newboard[:ind] + puzzle[newindex[ind]]
	return newboard

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

def playNow(): 
	global board
	gameOver = False
	playTurn = "X"
	while not gameOver: 
		if sys.argv[1] == "PP": 
			while playTurn == "X": 
				illegal = True
				while illegal:
					#print board
					posXSet = findPossibleMoves(playTurn, board)
					posOSet = findPossibleMoves("O", board)
					if not posXSet and not posOSet: 
						print "NO POSSIBLE MOVES! GAME OVER!"
						gameOver = True
					if not posXSet: 
						print "No Possible Moves!"
						print posXSet
						playTurn = "O"
						illegal = False
						break
					play = raw_input('X Turn ' )
					while play in dictTransform:
						play = play.lower()
						newboard = transform(play, board)
						showBoard(newboard)
						play = raw_input('X Turn ' )
						


					#print play
					#print type(play)
					index = int()
					#print posXSet
					if len(play) == 1: 
						quit()
					elif len(play) == 2: 
						index = int(play)
					elif len(play) == 3: 
						row = int(play[0])
						col = int(play[2])
						index = (8*row) + col
					elif len(play) == 4: 
						row = int(play[0])
						col = int(play[3])
						index = (8*row) + col 
					if index not in posXSet: 
						print posXSet
						#print neighDict[41]
						print "NOT A VALID MOVE"
					else: 
						board = board[:index] + "X" + board[index+1:]
						flipRest(index)
						showBoard(board)
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
						print "NO POSSIBLE MOVES! GAME OVER!"
						gameOver = True
					if not posOSet: 
						print "No Possible Moves!"
						print posOSet
						playTurn = "X"
						illegal = False
						break
					play = raw_input('O Turn ' )
					while play in dictTransform:
						play = play.lower()
						newboard = transform(play, board)
						showBoard(newboard)
						play = raw_input('O Turn ' )
					index = int()
					#print posOSet
					
					if len(play) == 1: 
						quit()
					elif len(play) == 2: 
						index = int(play)
					elif len(play) == 3: 
						row = int(play[0])
						col = int(play[2])
						index = (8*row) + col
					elif len(play) == 4: 
						row = int(play[0])
						col = int(play[3])
						index = (8*row) + col 
					if index not in posOSet: 
						print posOSet
						print "NOT A VALID MOVE"
					else: 
						board = board[:index] + "O" + board[index+1:]
						flipRest(index)
						showBoard(board)
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
	print "X Count " + str(xcount)
	print "O Count " + str(ocount)
	if xcount > ocount: 
		print "X WINS!"
	else: 
		print "O WINS!"


startGame()
createDictionary()
playNow()