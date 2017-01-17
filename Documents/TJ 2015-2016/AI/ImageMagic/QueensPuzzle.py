import sys 

N = sys.argv[1]

board = ["X" for k in range (N*N)]
# Q will be a queen 
# X will be a blank space 

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

board = makeDiagnol(board)
showBoard(board)

