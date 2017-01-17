import sys, string, time
startTime = time.clock()
wordCounter = 0
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
	if word in wordNeighborsDict:
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





print (format(wordCount()))
for neigh in neighborsDict.keys(): 
	print ("Neighbors: " + str(neigh) + "  Number of Words:  " + str(neighborsDict[neigh]))
print ("Run Time (secs)  " + str(time.clock() -startTime))


# mostNeighborsDict = {}
# def getNeighbors(word):
# 	if word in wordNeighborsDict:
# 		neighCount = 0
# 		for i in wordNeighborsDict[word]:
# 			neighCount += 1
# 		return neighCount

# def getTotalEdges():
# 	edgeCount = 0
# 	for word in wordNeighborsDict:
# 		for i in wordNeighborsDict[word]:
# 			edgeCount += 1
# 	return edgeCount/2

# components = []
# def breadthFirstSearch (): 
# 	queue = []
# 	checked = []
# 	for word in vertList:
# 		if word not in checked:
# 			checked.append(word)
# 			components.append([])
# 			components[len(components)-1].append(word)
# 			for i in wordNeighborsDict[word]:
# 				queue.append(i)
# 			while queue:
# 				curword = queue.pop(0)
# 				if curword not in checked:
# 					components[len(components)-1].append(curword)
# 					for k in wordNeighborsDict[curword]:
# 						queue.append(k)
# 					checked.append(curword)


# def largestComponent():
# 	size = 0
# 	for i in components:
# 		if(len(i) > size):
# 			size = len(i)
# 	return size

# componentsSizeDict = {} #key is the size, value is the number of components
# def componentSize():
# 	for i in components:
# 		if(len(i) in componentsSizeDict.keys()):
# 			componentsSizeDict[len(i)] += 1
# 		else: 
# 			componentsSizeDict[len(i)] = 1


# def mostNeighbors(): 
# 	mostNeighbors = 0
# 	mostWord = ""
# 	for i in vertList:
# 		if(getNeighbors(i) > mostNeighbors):
# 			mostNeighbors = getNeighbors(i)
# 			mostWord = i
# 	return mostWord + " has the most neighbors with " + str(mostNeighbors)

    

# print str(wordCount()) + " words in words.txt"
# #print getNeighbors(sys.argv[1]) + " neighbors of" + sys.argv[1]
# print str(getTotalEdges()) + " total edges!"
# breadthFirstSearch()
# print str(len(components)) + " components"
# print str(largestComponent()) + " size of the largest component"
# componentSize()
# for size in componentsSizeDict:
# 	print "Size: " + str(size) + "    # of components: " + str(componentsSizeDict[size])
# print mostNeighbors()













