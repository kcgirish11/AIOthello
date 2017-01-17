import sys, random
inboard = sys.argv[1]
char = sys.argv[2]
theE = '.'
theX = 'X'
theO = 'O'
##################################################
#
def ib( r , c ) :
   #
   return 0 <= r < 8 and 0 <= c < 8
   #
#
##################################################
#
def wouldBracket( theboard , thepiece , r , c , dr , dc ) :
   #
   theother = theX
   #
   if theother == thepiece : theother = theO
   #
   #
   #
   if ib( r + dr , c + dc ) :
      #
      j = ( r + dr ) * 8 + ( c + dc )
      #
      if theboard[j] == theother :
         #
         r += dr
         c += dc
         #
         while ib( r + dr , c + dc ) :
            #
            j = ( r + dr ) * 8 + ( c + dc )
            #
            if theboard[j] == thepiece : return True
            if theboard[j] == theE     : return False
            #
            r += dr
            c += dc
            #
         #
      #
   #
   return False
   #
#
##################################################
#
def thenBracket( theboard , thepiece , r , c , dr , dc ) :
   #
   theother = theX
   #
   if theother == thepiece : theother = theO
   #
   #
   #
   j = ( r + dr ) * 8 + ( c + dc )
   #
   while theboard[j] != thepiece :
      #
      theboard[j] =  thepiece
      #
      r += dr
      c += dc
      #
      j = ( r + dr ) * 8 + ( c + dc )
      #
   #
#
##################################################
#
def getPossMoves( theboard , thepiece ) :
   #
   #print ("IM HERE")
   alist = []
   #
   j = 0
   #
   while j < 64 :
      #
      if theboard[j] == theE :
         #
         r = j // 8 # row
         c = j %  8 # col
         #
         #          E   NE    N   NW    W   SW   S  SE
         drlist = [ 0 , -1 , -1 , -1 ,  0 ,  1 , 1 , 1 ]
         dclist = [ 1 ,  1 ,  0 , -1 , -1 , -1 , 0 , 1 ]
         #
         drc = zip( drlist , dclist )
         #
         for ( dr , dc ) in drc :
            #
            if wouldBracket( theboard , thepiece , r , c , dr , dc ) :
               #
               alist . append( j )
               #
               break
               #
            #
      #
      j += 1
      #
   #
   return alist
   #
#
##################################################

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

def flipRest(index, board):
	global neighDict 
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
	return board



#Total # of human pieces - # of computer pieces							
def boardScore(board): 
	oCount = 0
	xCount = 0
	for pos in range(len(board)): 
		if board[pos] == "O":
			oCount += 1 
		elif board[pos] == "X": 
			xCount += 1
	theOpp = "O"
	if char == "O": theOpp = "X" 
	theyHave = getPossMoves(board, theOpp)
	iHave = getPossMoves(board, char)
	if char == "X":
		return (len(iHave) - len(theyHave))*2 + (xCount - oCount)*.5
	else:
		return (len(iHave) - len(theyHave))*2 + (oCount - xCount)*.5

def minimax(depth, playTurn, board): 
	moves = getPossMoves(board, playTurn)
	bestMove = moves[0]
	bestScore = float('-inf')
	alpha = float('-inf')
	beta = float('inf')
	for position in moves: 
		fakeboard = board[:position] + playTurn + board[position+1:]
		flipped = flipRest(position, fakeboard)
		score = minPlay(depth-1, playTurn, flipped, alpha, beta)
		if score > bestScore: 
			bestMove = position
			bestScore = score
	return bestMove

def minPlay(depth, playTurn, board, alpha, beta): 
	if playTurn == "O": playTurn = "X"
	else: playTurn = "O" 
	if depth == 0: 
		return boardScore(board)
	moves = getPossMoves(board, playTurn)
	bestScore = float('inf')
	for position in moves: 
		fakeboard = board[:position] + playTurn + board[position+1:]
		flipped = flipRest(position, fakeboard)
		score = maxPlay(depth-1, playTurn, flipped, alpha, beta)
		if score < beta: 
			beta = score
		if beta < alpha: 
			return score
		if score < bestScore: 
			bestMove = position 
			bestScore = score
	return bestScore

def maxPlay(depth, playTurn, board, alpha, beta): 
	if playTurn == "O": playTurn = "X"
	else: playTurn = "O" 
	if depth == 0: 
		return boardScore(board) 
	moves = getPossMoves(board, playTurn)
	bestScore = float('-inf')
	for position in moves: 
		fakeboard = board[:position] + playTurn + board[position+1:]
		flipped = flipRest(position, fakeboard)
		score = minPlay(depth-1, playTurn, flipped, alpha, beta)
		if score > alpha: 
			alpha = score
		if beta < alpha: 
			return score
		if score > bestScore: 
			bestMove = position 
			bestScore = score
	return bestScore

def findIndex2(posSet, playTurn, board): 
	pos2MinNextMoves = {}
	for pos in posSet: 
		if playTurn == "X": 
			fakeboard = board[:pos] + "X" + board[pos+1:]
			posOSet = getPossMoves(fakeboard, "O")
			pos2MinNextMoves[pos] =  len(posOSet)
		else: 
			fakeboard = board[:pos] + "O" + board[pos+1:]
			posXSet = getPossMoves(fakeboard, "X")
			pos2MinNextMoves[pos] =  len(posXSet)
	pos = random.choice(list(posSet))
	leng = pos2MinNextMoves[pos]
	for p in pos2MinNextMoves: 
		if pos2MinNextMoves[p] < leng: 
			leng = pos2MinNextMoves[p]
			pos = p
	return pos

createDictionary()
print(minimax(4, char, inboard))

