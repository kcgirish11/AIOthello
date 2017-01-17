#nqueens genetic algorithm
import sys, math, random, time
startTime = time.clock()
poolSize = 50
N = 58

def findIntersect(board):
    count = 0
    perm = board
    #print(perm)
    length = len(perm)
    for ele1 in range(length):
        for ele2 in range(ele1+1, length):
            if abs(perm[ele1]-perm[ele2]) == abs(ele1-ele2):
                count += 1
            elif abs(perm[ele1]-perm[ele2]) == 0:
                count += 1
    return count


def printboard(board):
    lenboard = len(board)
    tstr = ""
    for char in board:
        for i in range(int(char)-1):
            tstr+=("* | ")
        tstr+='q'
        for i in range(lenboard-(int(char))):
            tstr+=(" | *")
        print(tstr)
        xstr = ""
        for i in range(len(tstr)-1):
            xstr+="-"
        print(xstr)
        tstr = ""
def derivedFitness(board): 
	return findIntersect(board)

def shuffle(board): 
	random.shuffle(board)
	return board

def getListOfParents(listOfBoards): 
	listOfParents = []
	for obj in listOfBoards: 
		(fit, par) = obj 
		listOfParents.append(par)
	return listOfParents


def permuteParents(initBoard):
	listOfBoards = [] 
	vector = initBoard
	for k in range(poolSize):
		shuffled = (shuffle(vector))
		#print (shuffled)
		derFit = derivedFitness(shuffled)
		if derFit == 0: 
			return [shuffled[:]]
		tup = (derFit, shuffled[:])
		#print (tup)
		listOfBoards.append(tup)
	return listOfBoards

def createInitBoard(): 
	board = []
	for n in range(N): 
		board.append(n+1)
	return board

def hasRepeats(baby): 
	if len(set(baby)) != len(baby): 
		return True
	else: 
		return False

def makeBaby(first, second): 
	#print (first)
	#print (second)
	pivot = random.randint(0, N)
	#print("pivot:", pivot)
	newBaby = first[:pivot+1]
	newBaby = newBaby + second[pivot+1:]
	if hasRepeats(newBaby):
		newBaby = makeBaby(first, second)
	return newBaby

def breed(listOfBoards):
	tempList = listOfBoards[:]
	listOfParents = getListOfParents(listOfBoards)
	for n in range(int(poolSize/2)): 
		(first, sec, ind1, ind2) = pickParents(tempList)
		getOut1 = tempList[ind1]
		getOut2 = tempList[ind2]
		tempList.remove(getOut1)
		tempList.remove(getOut2)
		newBaby = makeBaby(first, sec)
		baby = mutate(newBaby)
		while baby in listOfParents: 
			newBaby = makeBaby(first, sec)
			baby = mutate(newBaby) 
		listOfBoards.append((derivedFitness(baby), baby))
		if derivedFitness(baby) == 0: 
			listOfBoards = [baby]
			return listOfBoards
	return listOfBoards



def pickParents(listOfBoards):
	listOfBoards.sort()
	pSize =  len(listOfBoards)
	ind1 = random.randint(0, int(pSize/2))
	ind2 = random.randint(0, int(pSize/2))
	while ind1 == ind2: 
		ind2 = random.randint(0, int(pSize/2))

	(firstParDF, firstParVec) = listOfBoards[ind1]
	(secParDF, secParVec) = listOfBoards[ind2]
	#print ("FPV", firstParVec)
	#print ("SPV", secParVec)

	#makes sure both of the parents aren't the same list
		#print ("SPV", secParVec)
	return (firstParVec, secParVec, ind1, ind2)

def swap(board): 
	randPoint1 = random.randint(0, N-1) 
	randPoint2 = random.randint(0, N-1)
	#print (randPoint1)
	#print (randPoint2)
	#print (board)
	while randPoint1 == randPoint2: 
		randPoint2 = random.randint(0, N-1)
	temp = board[randPoint1]
	board[randPoint1] = board[randPoint2]
	board[randPoint2] = temp 
	return board


def mutate(board): 
	probabilty = random.randint(0, 10000)
	newBoard = board
	if probabilty >= 5000: 
		newBoard = swap(board)
	return newBoard

def killPeople(listOfBoards): 
	listOfBoards.sort() 
	initLeng = len(listOfBoards)
	diff = initLeng - poolSize
	for n in range(diff): 
		#print (initLeng - n-1)
		del listOfBoards[initLeng - n -1]
	return listOfBoards

def Start(): 
	board = createInitBoard()
	listOfBoards = permuteParents(board)
	goodBaby = board
	#print (listOfBoards)
	sameCount = 0
	generationCount = 0 
	same = listOfBoards[0]
	while len(listOfBoards) > 1: 
		generationCount += 1
		listOfBoards = breed(listOfBoards)
		listOfBoards = killPeople(listOfBoards)
		print (listOfBoards[0])
		if listOfBoards[0] != same: 
			sameCount = 0
			same = listOfBoards[0]
		else: 
			sameCount += 1
		#print (sameCount)
		if sameCount >= 1000: 
			listOfBoards = permuteParents(board)
		#print ("pass")
		#print (listOfBoards)
	#print (listOfBoards)
	goodBaby = listOfBoards[0]
	print ("GB", goodBaby)
	print (derivedFitness(goodBaby))
	print (generationCount)
	#print (goodBabyFit)

Start()
endTime = (time.clock() - startTime)
print (endTime)
 









