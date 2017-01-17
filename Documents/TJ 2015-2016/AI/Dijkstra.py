import sys, string, time, heapq
from Queue import PriorityQueue

wordCounter = 0
vertList = set(open("words.txt", "r").read().splitlines())
def wordCount():
	return len(vertList)

def relatedWords(word): 
	neighList = []
	for pos in range (len(word)):
		for letter in string.ascii_lowercase:   #checks if there is one letter difference
			neighbor = word[:pos] + letter + word[pos + 1:]
			if neighbor in vertList and word != neighbor: 
				neighList.append((1, neighbor))
		if(pos < 5):
			neigh = word[:pos] + word[pos+1] + word[pos] + word[pos+2:]
			if neigh in vertList:
				neighList.append((5, neigh))
	return neighList; 



wordNeighborsDict = {}
for word in vertList:
	neighbors = relatedWords(word)
	wordNeighborsDict[word] = neighbors

startTime = time.clock()

distance = {}
def Dijkstra(start):
	previous = {}
	queue = []
	visited = {}
	queue.append((0, start))
	distance[start] = 0
	for v in vertList: 
		if v is not start: 
			queue.append((10000,v))
			distance[v] = 10000
	heapq.heapify(queue)
	maxqueue = len(queue)
	while queue: 
		(dist, word) = heapq.heappop(queue)
		for n in wordNeighborsDict[word]:
			(dist2, word2) = n
			altdist = dist + dist2
			if altdist < distance[word2]:
				distance[word2] = altdist
				queue.append((altdist, word2))
				if len(queue) > maxqueue:
					maxqueue = len(queue)
				previous[word2] = word
				visited[word2] = True
				
	return (previous, maxqueue, visited)

#print format(wordCount())
path = []
word = sys.argv[1]
target = sys.argv[2]
(x,y,z) = Dijkstra(word)
pathDict = x
visited = z
#print pathDict[target]
if target not in visited: 
 	print "These words are not connected"
else:
	pathweight = distance[target]
	while target != word: 
		path.append(target)
		target = pathDict[target]
	path.append(word)
	print list(reversed(path))
	print "Path Length: " + str(pathweight)
	print "Maximum Length of queue:  " + str(y)
	print "Number of nodes visited:  " + str(len(visited.keys()))
print "Run Time (secs)  " + str(time.clock() -startTime)
