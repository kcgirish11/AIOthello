import sys, string, time

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


wordNeighborsDict = {}
for word in vertList:
	neighbors = relatedWords(word)
	wordNeighborsDict[word] = neighbors

pathDict = {}
def DFS(vert, end): 
	vertcount = 0
	maxleng= 0
	checked = {word1:False for word1 in wordNeighborsDict}
	stack = []
	stack.append(vert)
	vertcount+=1
	if vert == end:
		return 0
	while stack:
		if(len(stack) > maxleng):
			maxleng = len(stack)
		v = stack.pop()
		if checked[v] is False:
			if v == end:
				return (vertcount, maxleng)
			checked[v] = True
			vertcount += 1
			for n in wordNeighborsDict[v]:
				if checked[n] == False:
					stack.append(n)
					pathDict[n] = v
				#print stack
	return (0,0)

#print format(wordCount())
path = []
word = sys.argv[1]
target = sys.argv[2]
startTime = time.clock()
(x,y) = DFS(word, target)
if(x==0 and y==0):
	print "Sorry. These words don't have a path connecting them!"
else:
	while word != target:
		path.append(target)
		target = pathDict[target]	
		#print target
	path.append(word)
	print list(reversed(path))
	print "Path Length: " + str(len(path) - 1)
	print "Vertices visited: " + str(x)
	print "Max Length of Queue:  " + str(y)
#print "Diameter: " + format(diameter())
print "Run Time (secs):  " + str(time.clock() -startTime)
