import sys, time, math
guessCount = 0
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
			if pos == 46: 
				print notfound
			if len(notfound) == 1:
				puzzle = puzzle[:pos] + notfound.pop() + puzzle[pos+1:]
				if pos == 46: 
					print "adding the 8 now"
					print notfound
					print showDetails(puzzle)

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
					#print pos
					#print puzzle[pos]
					return False
				else:
					visited.add(puzzle[pos])
	return True


def makeDeductions(puzzle): 
	#print "BEFORE: %s" % puzzle
	(puzzle, dictP) = findPossible(puzzle)
	#print puzzle
	for grp in groups:
		showDetails(puzzle)
		sym2count = {sym1: set() for sym1 in allSyms}
		for pos in grp: 
			if pos in dictP: 
				for k in dictP[pos]: 
					sym2count[k].add(pos)

		#print sym2count
		#print sym2count
		for sym in allSyms:
			if len(sym2count[sym]) == 1: 
				pos = sym2count[sym].pop()
				#print "POS" + format(pos)
				#print "SYM" + format(sym)
				for neigh in cellNeighbors[pos]: 
					if neigh in dictP:
						if sym in dictP[neigh]: 
							#print "POS " + format(pos)
							dictP[neigh] -= {sym}
							if pos == 46:
								print "REMOVED"
								print sym
								print neigh
								print dictP
				puzzle = puzzle[:pos] + sym + puzzle[pos+1:] 
				#showDetails(puzzle) 
				print "SECOND"
				print grp
				if validateSudoku(puzzle): 
					print "YAY"
					#showBoard(puzzle)
				else: 
					showDetails(puzzle)
					quit()
				if pos in dictP:
					del dictP[pos]
					#print dictP
	#print "AFTER: %s" % puzzle
	return (puzzle, dictP)

def dctPsblGet(puzzle):
  # identify relevant lengths
  sideLen = int(math.sqrt(len(puzzle)))
  smaller = int(math.sqrt(sideLen))
  while (sideLen/smaller != int(sideLen/smaller)): smaller -= 1
  larger = int(sideLen/smaller)

  # list of all possible symbols (with larger sudokus)
  syms = "".join(list(set(puzzle)-{'.'})) + "123456789ABCDE0FGHIFKLMNOPQRSTUVWXYZ"
  for pos in range(sideLen, len(syms)):
    if len(set(syms[:pos]))==sideLen:
      allSyms = set(syms[:pos])
      break

  # cellNeighbors
  cellNeighbors = [set() for dummy in range(len(puzzle))]
  for colPos in range(0,sideLen):     # this section does rows and columns
    for rowStart in range(0, len(puzzle), sideLen):
      cellNeighbors[rowStart+colPos] |= set(range(rowStart, rowStart+sideLen))
      cellNeighbors[rowStart+colPos] |= set(range(colPos, len(puzzle), sideLen))
  # this section does the inner blocks
  blkOffs = [blkRow + blkCol for blkRow in range(0, len(puzzle), smaller*sideLen)
                             for blkCol in range(0, sideLen,larger)]
  for blkOff in blkOffs:
    lstPos = [blkOff + rowOff + colPos
                     for rowOff in range(0, smaller*sideLen, sideLen)
                     for colPos in range(larger)]
    for pos in lstPos: cellNeighbors[pos] |= set(lstPos)

  # finally, compute the dictionary of possible
  # symbols for each unfilled position
  dctPsbl = {pos:allSyms - {puzzle[sq] for sq in cellNeighbors[pos]}
                  for pos in range(len(puzzle)) if puzzle[pos]=='.'}
  return dctPsbl

def rowDetail(puzzle, dctPsbl, rowNum, longer):
  # returns the output to be printed for a given row
  sideLen = int(math.sqrt(len(puzzle)))
  rowStartPos = rowNum * sideLen

  # This section constructs the raw possibilities string
  aPossArray = [[' ' for dummyi in range(sideLen)] for dummyo in range(sideLen)]
  for pos in range(rowStartPos,rowStartPos+sideLen):
    if puzzle[pos]!='.':
      aPossArray[pos % sideLen][int((sideLen+2)/2)-(sideLen % 2)] = puzzle[pos]
    else:
      if pos in dctPsbl:
        for i in range(len(dctPsbl[pos])):
          aPossArray[pos % sideLen][i] = sorted(list(dctPsbl[pos]))[i]

  # Now assemble the output
  aOut = ['' for dummy in range(sideLen)]
  outStr = ""
  aLine = []
  for subRow in range(0,sideLen,longer):
    aLine.append(["".join(aPossArray[colNum])[subRow:subRow+longer] for colNum in range(sideLen)])
    for idx in range(longer,sideLen,longer): aLine[-1][idx-1]+="|"
  outStr = "\n".join(["|".join(aLine[idx]) for idx in range(len(aLine))]) + "\n"
  return outStr


def showDetails(puzzle):
  # first get sizing information
  sideLen = int(math.sqrt(len(puzzle)))
  smaller = int(math.sqrt(sideLen))
  while (sideLen/smaller != int(sideLen/smaller)): smaller -= 1
  longer = int(sideLen/smaller)
  dctPsbl = dctPsblGet(puzzle)

  # define the row separators
  aSepInner = [("-" * longer) for dummy in range(sideLen)]
  for idx in range(longer,sideLen,longer): aSepInner[idx-1]+="+"
  rowSep = "+".join(aSepInner) + "\n"        # row separator
  rowSepMajor = rowSep.replace("-", "=")     # row separator between blocks

  # determine the row content
  aRowsToShow = [rowDetail(puzzle, dctPsbl, rowNum, longer) for rowNum in range(sideLen)]
  for insertAt in reversed(range(1,sideLen)):
    aRowsToShow[insertAt:insertAt] = [rowSep]

  # now display it
  for rewriteAt in reversed(range(longer,sideLen,longer)):
    aRowsToShow[2*rewriteAt-1] = rowSepMajor
  print "\n"+("".join(aRowsToShow))[:-1]

def bruteForce(puzzle):
	#print "GOT HERE"
	#showBoard(puzzle)
	print "BEGIN"
	showDetails(puzzle)
	guessCount += 1
	global guessCount
	#print puzzle
	(puzzle, dictP) = makeDeductions(puzzle)
	#print puzzle
	showBoard(puzzle)
	if validateSudoku(puzzle) == False:
		return ""
	pos = puzzle.find(".")
	if pos < 0:
		return puzzle
		'''
		if validateSudoku(puzzle): 
			return puzzle
		else: 
			return ""
		'''
	for key in dictP: 
		if (len(dictP[key]) < len(dictP[pos])):
			pos = key
	#print puzzle
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



