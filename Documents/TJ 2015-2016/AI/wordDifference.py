import sys, urllib
link = "https://academics.tjhsst.edu/compsci/ai/words.txt"
hFile = urllib.urlopen(link)
wordCounter = 0
vertList = []
for line in hFile: 
	myWord = line.rstrip("\n")
	vertList.append(myWord)
	wordCounter+=1
def wordCount():
	return wordCounter

def wordDifference(str1, str2):
	diffCheck = False
	if len(str1) == len(str2):
		for i in range (len(str1)):
			if str1[i] != str2[i] and diffCheck == False:
				diffCheck = True
			elif str1[i] != str2[i]:
				return 0
		return 1

	else:
		return -1




wordNeighborsDict = {}
for word in vertList:
	neighbors = []
	wordNeighborsDict[word] = neighbors
	for comp in vertList: 
		if(wordDifference(word, comp) == 1) and word != comp:
			neighbors.append(comp)



def getNeighbors(word):
	if word in wordNeighborsDict:
		neighCount = 0
		for i in wordNeighborsDict[word]:
			neighCount += 1
			#print i
		return (str(neighCount) + " neighbors of " + word)
	else: 
		return "This is not a six-letter word"

def getTotalEdges():
	edgeCount = 0
	for word in wordNeighborsDict:
		for i in wordNeighborsDict[word]:
			edgeCount += 1
	return edgeCount/2


print str(wordCount()) + " words in words.txt"
print getNeighbors(sys.argv[1])
print str(getTotalEdges()) + " total edges!"







