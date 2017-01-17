import sys, time, math
guessCount = 0
puzzleList = open("sudoku141.txt", "r").read().splitlines()
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
		allSyms.append(str(n+1))


def cellNeigh(puzzle): 
	global groups
	global cellNeighbors
	cellNeighbors = [set().union(*[set(grp) for grp in groups if pos in grp ])- {pos} for pos in range(len(puzzle))]
	#print cellNeighbors


def findPossible(puzzle):
	dictPos = {}
	global cellNeighbors
	#print cellNeighbors
	for pos in range(len(puzzle)):
		if puzzle[pos] == ".": 
			#print cellNeighbors[pos]
			found = set(puzzle[index] for index in cellNeighbors[pos] if puzzle[index] != ".")
			#print found
			notfound = set(sym for sym in allSyms if sym not in found)
			#print notfound
			if len(notfound) == 1:
				puzzle = puzzle[:pos] + notfound.pop() + puzzle[pos+1:]
			else: 
				dictPos[pos] = notfound
	#print dictPos
	return (puzzle,dictPos)


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


def makeDeductions(puzzle): 
	(puzzle, dictP) = findPossible(puzzle)
	for grp in groups: 
		sym2count = {sym1: set() for sym1 in allSyms}
		for pos in grp: 
			if pos in dictP: 
				for k in dictP[pos]: 
					sym2count[k].add(pos)
		for sym in sym2count: 
			if len(sym2count[sym]) == 1: 
				pos = sym2count[sym].pop()
				for neigh in cellNeighbors[pos]: 
					if neigh in dictP:
						if sym in dictP[neigh]: 
							dictP[neigh].remove(sym)
				puzzle = puzzle[:pos] + sym + puzzle[pos+1:] 
	return (puzzle, dictP) 		

def bruteForce(puzzle):
	#print "GOT HERE"
	#showBoard(puzzle)
	guessCount += 1
	global guessCount
	(puzzle, dictP) = findPossible(puzzle)
	pos = puzzle.find(".")
	for key in dictP: 
		if (len(dictP[key]) < len(dictP[pos])):
			pos = key
	#print puzzle
	if pos < 0:
		return puzzle
	for c in dictP[pos]:
		#print puzzle[:pos] + c + puzzle[pos+1:]
		bf = bruteForce(puzzle[:pos] + c + puzzle[pos+1:])
		#print bf
		if bf != "":
			return bf
	return ""



positions(9)
symbols()
if len(sys.argv) == 2:
	startTime = time.clock()
	puzzleLine = int(sys.argv[1])
	puzzle = puzzleList[puzzleLine -1]
	showBoard(puzzle)
	print "SOLUTION BOARD"
	cellNeigh(puzzle)
	puzzle = bruteForce(puzzle)
	#print puzzle
	showBoard(puzzle)
	print "Run time (seconds): " + format(time.clock() - startTime)
elif len(sys.argv) == 3: 
	puzzleStart = int(sys.argv[1])
	puzzleStop = int(sys.argv[2])
	for i in range(puzzleStart, puzzleStop+1, 1): 
		print "PUZZLE NUMBER " + str(i)
		puzzle = puzzleList[i-1]
		print puzzle
		cellNeigh(puzzle)
		puzzle = bruteForce(puzzle)
		#print "SOLUTION"
		print puzzle
		print 
elif len(sys.argv) == 1: 
	count = 1
	startTime = time.clock()
	for puzzle in puzzleList:
		print "PUZZLE NUMBER " + str(count)
		count+=1
		print
		startPuzzTime = time.clock()
		print puzzle
		cellNeigh(puzzle)
		puzzle = bruteForce(puzzle)
		#print "SOLUTION"
		print puzzle
		print "Run time(seconds): " + format(time.clock() - startPuzzTime)
		print  
	print "Number of guesses: " + format(guessCount)
	print "Overall run time (seconds): " + format(time.clock() - startTime)


		
else: 
	print "INVALID INPUT"



