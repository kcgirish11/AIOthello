
import sys

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

#print string

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
			if pos % 8 != 1 and pos != 63: 
				neigh.add(pos-7)
		if pos % 8 != 0:  #left
			neigh.add(pos-1)
		if (pos % 8 != 1 and pos != 63 and pos != 7) or pos == 1:  #right
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

board = sys.argv[1]
player = sys.argv[2]
showBoard(board)
createDictionary()
#print neighDict
print "Possible Moves" 
for move in findPossibleMoves(player, board): 
	board = board[:move] + "*" + board[move+1:]
showBoard(board)