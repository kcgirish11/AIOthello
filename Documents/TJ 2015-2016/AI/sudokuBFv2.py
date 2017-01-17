import sys, time, math
puzzleList = open("sudoku128.txt", "r").read().splitlines()
def showBoard(puzzle):
	lineleng = int(math.sqrt(len(puzzle)))
	#print len(puzzle)
	count = 0
	for k in range(lineleng+2):
		line = ""
		if k == 3 or k == 7:
			for z in range(lineleng):
				line = line + "-"
		else: 
			for i in range(lineleng+2):
				if i == 3 or i == 7:
					line = line + "|"
				else: 
					line = line + puzzle[count]
					count += 1
		print line
def checkBlock(r, c):
	if r < 3 and c < 3: 
		return 0
	elif r < 3 and c >= 3 and c < 6:
		return 1
	elif r < 3 and c >= 6 and c < 9: 
		return 2
	elif r >= 3 and r < 6 and c < 3:
		return 3
	elif r >= 3 and r < 6 and c >= 3 and c < 6:
		return 4
	elif r >= 3 and r < 6 and c >= 6 and c < 9:
		return 5
	elif r >= 6 and r < 9 and c < 3:
		return 6
	elif r >= 6 and r < 9 and c >= 3 and c < 6:
		return 7
	elif r >= 6 and r < 9 and c >= 6 and c < 9:
		return 8


def validateSudoku(puzzle):
	lineleng = int(math.sqrt(len(puzzle)))
	count = 0
	#print "GOT HERE"
	mat = [[0 for x in range(lineleng)] for x in range(lineleng)] 	
	for r in range(lineleng):
		for c in range(lineleng):
			mat[r][c] = puzzle[count]
			#print puzzle[count]
			count += 1
	visitedRow = {}
	visitedCol = {}
	visitedBlock = {}
	for k in range(lineleng):
		visitedRow[k] = []
		visitedCol[k] = []
		visitedBlock[k] = []
	for r in range(lineleng):
		for c in range(lineleng): 
			b = checkBlock(r,c)
			if mat[r][c] in visitedRow[r] or mat[r][c] in visitedCol[c] or mat[r][c] in visitedBlock[b]: 
				#print "Boo"
				return False
			else:
				#print "HERE"
				visitedRow[r].append(mat[r][c])
				visitedCol[c].append(mat[r][c])
				visitedBlock.append(mat[r][c])
	#print "hi"
	return True

		

def bruteForce(puzzle):
	#print "GOT HERE"
	#showBoard(puzzle)
	if not validateSudoku(puzzle):
		return ""
	pos = puzzle.find(".")
	if pos < 0:
		return puzzle
	for c in "123456789":
		#print puzzle[:pos] + c + puzzle[pos+1:]
		bf = bruteForce(puzzle[:pos] + c + puzzle[pos+1:])
		#print bf
		if bf != "":
			return bf
	return ""


if len(sys.argv) > 0:
	puzzleLine = int(sys.argv[1])
	puzzle = puzzleList[puzzleLine -1]
	showBoard(puzzle)
	print "NEXT BOARD"
	puzzle = bruteForce(puzzle)
	#print puzzle
	showBoard(puzzle)
