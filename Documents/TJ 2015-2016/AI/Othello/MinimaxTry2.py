import sys
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
	if char == "X": 
		return xCount - oCount
	elif char == "O":
		return oCount - xCount

def minimax(depth, playTurn, board): 
	moves = getPossMoves(board, playTurn)
	bestMove = moves[0]
	bestScore = float('-inf')
	for position in moves: 
		fakeboard = board[:position] + playTurn + board[position+1:]
		flipped = flipRest(position, fakeboard)
		score = minPlay(depth-1, playTurn, flipped)
		if score > bestScore: 
			bestMove = position
			bestScore = score
	return bestMove

def minPlay(depth, playTurn, board): 
	if playTurn == "O": playTurn = "X"
	else: playTurn = "O" 
	if depth == 0: 
		return boardScore(board)
	moves = getPossMoves(board, playTurn)
	bestScore = float('inf')
	for position in moves: 
		fakeboard = board[:position] + playTurn + board[position+1:]
		flipped = flipRest(position, fakeboard)
		score = maxPlay(depth-1, playTurn, flipped)
		if score < bestScore: 
			bestMove = position 
			bestScore = score
	return bestScore

def maxPlay(depth, playTurn, board): 
	if playTurn == "O": playTurn = "X"
	else: playTurn = "O" 
	if depth == 0: 
		return boardScore(board) 
	moves = getPossMoves(board, playTurn)
	bestScore = float('-inf')
	for position in moves: 
		fakeboard = board[:position] + playTurn + board[position+1:]
		flipped = flipRest(position, fakeboard)
		score = minPlay(depth-1, playTurn, flipped)
		if score > bestScore: 
			bestMove = position 
			bestScore = score
	return bestScore

createDictionary()
print(minimax(3, char, inboard))

# def maxValue(depth, playTurn, board):
# 	tuplesofPosMoves = [] 
# 	if playTurn == "O": playTurn = "X"
# 	else: playTurn = "O" 
# 	for pos in findPossibleMoves(playTurn, board): 
# 		fakeboard = board[:pos] + playTurn + board[pos+1:]
# 		flipped = flipRest(pos, fakeboard)
# 		childValue = 0
# 		if depth == 0: 
# 			childValue = boardScore()
# 		elif depth != 0: 
# 			childValue = minValue(depth-1, playTurn, flipped)
# 		tuplesofPosMoves.append(childValue)
# 	if tuplesofPosMoves: 
# 		return max(tuplesofPosMoves)
# 	elif depth == 0: 
# 		return boardScore()
# 	else: 
# 		return minValue(depth-1, playTurn, board)
# def minValue(depth, playTurn, board):
# 	tuplesofPosMoves = [] 
# 	if playTurn == "X": playTurn = "O"
# 	else: playTurn = "X"
# 	for pos in findPossibleMoves(playTurn, board): 
# 		fakeboard = board[:pos] + playTurn + board[pos+1:]
# 		flipped = flipRest(pos, fakeboard) 
# 		childValue = 0
# 		if depth == 0: 
# 			childValue = boardScore()
# 		elif depth != 0: 
# 			childValue = maxValue(depth-1, playTurn, flipped)
# 		tuplesofPosMoves.append(childValue)
# 	if tuplesofPosMoves: 
# 		return min(tuplesofPosMoves)
# 	elif depth == 0: 
# 		return boardScore()
# 	else: 
# 		return maxValue(depth-1, playTurn, board)

# createDictionary()
# posSet = findPossibleMoves(char,board)
# if len(posSet) == 1: 
# 	print (posSet.pop())
# else:
# 	tuplesForreal = []
# 	for pos in posSet:
# 		fakeboard = board[:pos] + char + board[pos+1:]
# 		flipped = flipRest(pos, fakeboard) 
# 		value = maxValue(3, char, flipped)
# 		tuplesForreal.append((value, pos))
# 	if tuplesForreal: 
# 		(val, posIwant) = min(tuplesForreal)
# 		print (posIwant)




				
