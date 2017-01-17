import sys, string, time
startTime = time.clock()
vertList = set(open("words.txt", "r").read().splitlines())
def wordCount():
	return len(vertList)

def relatedWords(word): 
	neighList = []
	for pos in range (len(word)):
		for letter in string.ascii_lowercase:  
			neighbor = word[:pos] + letter + word[pos + 1:]
			if neighbor in vertList and word != neighbor: 
				neighList.append(neighbor)
	return neighList; 



neighborsDict = {}
def getNeighbors(word):
	if word in wordNeighborsDict.keys():
		neighCount = 0
		for i in wordNeighborsDict[word]:
			neighCount += 1
		if neighCount in neighborsDict: 
			neighborsDict[neighCount] +=1
		else: 
			neighborsDict[neighCount] = 1
		return neighCount

wordNeighborsDict = {}
for word in vertList:
	neighbors = relatedWords(word)
	wordNeighborsDict[word] = neighbors
	getNeighbors(word)




def mostNeighbors(): 
	mostNeighbors = 0
	mostWord = ""
	for i in vertList:
		if(getNeighbors(i) > mostNeighbors):
			mostNeighbors = getNeighbors(i)
			mostWord = i
	return mostWord + " has the most neighbors with " + str(mostNeighbors)


def getTotalEdges():
	edgeCount = 0
	for word in wordNeighborsDict:
		for i in wordNeighborsDict[word]:
			edgeCount += 1
	return edgeCount/2

components = []
levelDict = {}
pathDict = {}
def breadthFirstSearch (): 
	queue = []
	checked = []
	for word in vertList:
		if word not in checked:
			checked.append(word)
			components.append([])
			components[len(components)-1].append(word)
			for i in wordNeighborsDict[word]:
				queue.append(i)
			while queue:
				curword = queue.pop(0)
				if curword not in checked:
					components[len(components)-1].append(curword)
					for k in wordNeighborsDict[curword]:
						queue.append(k)
					checked.append(curword)


componentsDict = {}	
def makeComponentsDict():
	for comps in components: 
		for word in comps: 
			componentsDict[word] = comps



def searchFarthest(word):
	farWord = ""
	comp = componentsDict[word]
	startlevel = levelDict[word]
	print startlevel
	for n in comp: 
		if levelDict[n] > startlevel:
			farWord = n
			startlevel = levelDict[n]
	print farWord
	return farWord

def BFSfarthest(word): 
	queue = []
#	checked = {}
#	for word1 in wordNeighborsDict:
#		checked[word1] = False
	checked = {word1:False for word1 in wordNeighborsDict}
	farthest = ""
	distance = 0
	checked[word] = True

	for i in wordNeighborsDict[word]:
		queue.append((i, word, 1))
	while queue:
		(x,y,z)= queue.pop(0)
		curword = x
		if checked[curword] is False:
			pathDict[curword] = y
			farthest = curword
			distance = z
			for k in wordNeighborsDict[curword]:
				if checked[k] == False:
					queue.append((k,curword, z+1))
			checked[curword] = True
	return (farthest, distance)


def largestComponent():
	size = 0
	for i in components:
		if(len(i) > size):
			size = len(i)
	return size

componentsSizeDict = {} #key is the size, value is the number of components
def componentSize():
	for i in components:
		if(len(i) in componentsSizeDict.keys()):
			componentsSizeDict[len(i)] += 1
		else: 
			componentsSizeDict[len(i)] = 1


def diameter(): 
	diacount = 0
	diameter = 0
	startword = ""
	for word in wordNeighborsDict.keys():
		(x,y) = BFSfarthest(word)
		startword = word
		diacount = y
		far = x
		if diacount > diameter:
			diameter = diacount
			
	#print startword
	return (diameter, startword, far)
#print str(wordCount()) + " words in words.txt"
#print getNeighbors(sys.argv[1]) + " neighbors of" + sys.argv[1]
#print str(getTotalEdges()) + " total edges!"
# print mostNeighbors()
# for neigh in neighborsDict.keys(): 
# 	print str(neighborsDict[neigh]) + " words have "+ str(neigh) + "  neighbors"
breadthFirstSearch()
makeComponentsDict()
if(len(sys.argv) - 1) == 1:
	pathDist = 0
	print sys.argv[1]
	(x,y) = BFSfarthest(sys.argv[1])
	print x
	path = []
	#path.append(farword)
	while x != sys.argv[1]:
		x = pathDict[x]
		print x
	print "Distance: " + str(y)
	#print list(reversed(path))
elif(len(sys.argv) -1) == 2: 
	path = []
	pathDist = 1
	word1 = sys.argv[1]
	word2 = sys.argv[2]
	BFSfarthest(word1)
	path.append(word2)
	while pathDict[word2] != word1:
		word2 = pathDict[word2]
		path.append(word2)
		pathDist+=1
	path.append(word1)
	print "Distance: " + str(pathDist)
	print list(reversed(path))
elif (len(sys.argv) - 1) == 0:
	print str(len(components)) + " components"
	(x,y,z) = diameter()
	path = []
	#print y
	#print z
	print "Diameter:  " + str(x)
	while z != y:
		path.append(z)
		z = pathDict[z]
	path.append(y)
	print list(reversed(path))

	print str(largestComponent()) + " size of the largest component"
	componentSize()
	
	for size in componentsSizeDict:
		print "Size: " + str(size) + "    # of components: " + str(componentsSizeDict[size])
print "Run Time (secs)  " + str(time.clock() -startTime)















