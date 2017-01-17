import sys, random, math
import numpy as np
from itertools import permutations


swapCount = 0 
shuffleCount = 0 
lateralSwap = 0 
avgSwap = 0 
avgShuffle = 0 
avgLateral = 0


N = int(sys.argv[1])

board = ["X" for k in range (N*N)]
# Q will be a queen 
# X will be a blank space 

def createPerm(): 
	pString = []
	for k in range(N): 
		pString.append(k+1)
	return pString


def showBoard(board): 
	print "   ", 
	for l in range(N): 
		print "-",
	print
	for i in range(N): 
		print i,
		print "|",
		for k in range(N):  
			print board[i*N + k], 
		print "|",
		print i
	print "   ", 
	for l in range(N): 
		print "-",
	print
	print "   ",
	for m in range(N): 
		print m,
	print

def makeDiagnol(board):
	for pos in range (N): 
		board[(pos*N) + pos] = "Q"
	return board 

def getQueenPositions(board):
	positions = [] 
	for pos in range(N*N): 
		if board[pos] == "Q": 
			positions.append(pos)
	return positions


def rowConflicts(board):
	conflictCount = 0
	for row in range (N): 
		queenCount = 0
		for col in range (N):
			if board[row*N + col] == "Q": 
				queenCount += 1
		if queenCount > 1: 
			conflictCount += 1
	return conflictCount

def colConflicts(board): 
	conflictCount = 0 
	for col in range(N): 
		queenCount = 0 
		up = col
		if board[up] == "Q": 
			queenCount += 1	
		for k in range(N-1): 
			up = up + N
			if board[up] == "Q": 
				queenCount += 1	
		if queenCount > 1: 
			conflictCount += 1
	return conflictCount

def convertToMatrix(board):
	matrixBoard = [[0 for n in range(N)] for n in range(N)]
	for row in range(N): 
		for col in range(N): 
			matrixBoard[row][col] = board[row*N + col]
	return matrixBoard

def diagConflicts(perm_string): 
	conflictCount = 0 
	#print(perm_string)
	for queen in range(len(perm_string)): 
		for queen2 in range(len(perm_string)):
			if queen != queen2: 
				row1 = int(queen)
				col1 = int(perm_string[queen])
				row2 = int(queen2)
				col2 = int(perm_string[queen2])
				#print(row1)
				#print(row2)
				if (math.fabs(row1 - row2) == math.fabs(col1 - col2)):
					conflictCount += 1
	return conflictCount

def convertPermToBoard(perm_string): 
	local_board = ["X" for k in range (N*N)]
	for col in range(len(perm_string)): 
		#print(perm_string, "perm")
		row = int(perm_string[col]) - 1
		#print (row, "row")
		#print(col, "col")
		#print ((row*N)+col, "here")
		local_board[row*N + col] = "Q"
	return local_board


def swap(perm_string): 
	global swapCount
	#print("perm", perm_string)
	newString = perm_string
	initConf = findConflicts(perm_string)
	for q in range(len(perm_string)): 
		for  q2 in range(q,len(perm_string)):
			newString = perm_string
			temp = newString[q]
			newString[q] = newString[q2]
			newString[q2] = temp 
			swapCount += 1
			conf = findConflicts(newString)
			#print(conf, newString)
			if conf < initConf: 
				initConf = conf
			if conf == 0: 
				return (newString, initConf)
	return (newString, initConf)


def shuffle():
	global shuffleCount 
	shuffleCount += 1
	newList = []
	while len(newList) != N: 
		term = random.randrange(1, N+1)
		if term not in newList:
			newList.append(term)
	return newList

def permutation(perm_string):
	global lateralSwap
	curPerm = perm_string
	curConflict = findConflicts(curPerm)
	while curConflict != 0: 
		pastConflict = 0
		while curConflict > pastConflict: 
			(pString, conf) = swap(curPerm)
			if conf == 0: 
				return (pString, conf)
			if conf == curConflict: 
				lateralSwap += 1
			curPerm = pString
			pastConflict = curConflict
			curConflict = conf
		curPerm = shuffle()
	return(curPerm, curConflict)

def findConflicts(perm):
	#print(rowConflicts(board))
	#print (colConflicts(board))
	#print (diagConflicts(board)) 
	return  diagConflicts(perm)



#board = makeDiagnol(board)
#showBoard(board)
#perm = [2,4,6,1,3,5]
#print(diagConflicts(perm))
# board = convertPermToBoard(perm)
# showBoard(board)
# print (perm)
trials = 100
for t in range(trials): 
	swapCount = 0 
	shuffleCount = 0 
	lateralSwap = 0 
	perm = createPerm()
	(new_perm, conflictN) = (permutation(perm))
	avgSwap += swapCount
	avgShuffle += shuffleCount
	avgLateral += lateralSwap



#board = convertPermToBoard(new_perm)
#print("Permutation String", new_perm)
#showBoard(board)
print (trials)
print ("Avg Swaps: ", (avgSwap/trials))
print ("Shuffles: ", (avgShuffle/ trials))
print ("Lateral: ", (avgLateral/trials))



