import sys, time, math
startTime = time.clock()
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


groups = []
def positions(lineleng):
	#rows
	group = []
	for i in range(lineleng*lineleng+1):
		if i % 9 == 0 and i != 0:
			groups.append(group)
			group = []
		if i != 81:
			group.append(i)
	
	#cols
	for i in range(lineleng): 
		group.append(i)
		up = i
		for k in range(lineleng-1): 
			up = up + lineleng
			group.append(up)
		groups.append(group)
		group = []
	#print groups

	#blocks
	for row in range(3):
		for col in range(3):
			box = []
			for i in range(3):
				for j in range(3): 
					box.append((3*row + i)*9 + (3*col + j))
			groups.append(box)
	#print groups

allSyms = []
def symbols(): 
	for n in range(9): 
		allSyms.append(n+1)




def validateSudoku(puzzle):
	lineleng = int(math.sqrt(len(puzzle)))
	for g in groups:
		visited = set()
		for pos in g: 
			#print pos
			if puzzle[pos] != ".":
				if puzzle[pos] in visited: 
					return False
				else:
					visited.add(puzzle[pos])
	return True

		

def bruteForce(puzzle):
	#print "GOT HERE"
	#showBoard(puzzle)
	if not validateSudoku(puzzle):
		return ""
	pos = puzzle.find(".")
	#print puzzle
	if pos < 0:
		return puzzle
	for c in "123456789":
		#print puzzle[:pos] + c + puzzle[pos+1:]
		bf = bruteForce(puzzle[:pos] + c + puzzle[pos+1:])
		#print bf
		if bf != "":
			return bf
	return ""

positions(9)
if len(sys.argv) == 2:
	puzzleLine = int(sys.argv[1])
	puzzle = puzzleList[puzzleLine -1]
	showBoard(puzzle)
	print "SOLUTION BOARD"
	puzzle = bruteForce(puzzle)
	#print puzzle
	showBoard(puzzle)
elif len(sys.argv) == 3: 
	puzzleStart = int(sys.argv[1])
	puzzleStop = int(sys.argv[2])
	for i in range(puzzleStart, puzzleStop+1, 1): 
		print "PUZZLE NUMBER " + str(i)
		puzzle = puzzleList[i-1]
		print puzzle
		puzzle = bruteForce(puzzle)
		#print "SOLUTION"
		print puzzle
		print 

		
else: 
	print "INVALED INPUT"

print "Run time (seconds): " + format(time.clock() - startTime)

