import sys, time, heapq
from math import pi , acos , sin , cos
cityList = set(open("romFullNames.txt", "r").read().splitlines())
letter2city = {}
city2letter = {}
for c in cityList: 
	letter2city[c[0]] = c
	city2letter[c] = c[0]

nodes = open("romNodes.txt", "r").read().splitlines()
node2coordinate = {}
for n in nodes:
	arr = n.split()
	node2coordinate[arr[0]] = (float(arr[1]), float(arr[2]))

edges = open("romEdges.txt", "r").read().splitlines()
node2neigh = {}
for e in edges: 
	a = e.split()
	if a[0] not in node2neigh:
		node2neigh[a[0]] = []
	node2neigh[a[0]].append(a[1])
	if a[1] not in node2neigh: 
		node2neigh[a[1]] = []
	node2neigh[a[1]].append(a[0])



def costCalc(start, end):
	(x1, y1) = node2coordinate[start]
	(x2, y2) = node2coordinate[end]
	if start == end: 
		return 0
	y1  = float(y1)
	x1  = float(x1)
	y2  = float(y2)
	x2  = float(x2)
	r   = 3958.76 # miles
	y1 *= pi/180.0
	x1 *= pi/180.0
	y2 *= pi/180.0
	x2 *= pi/180.0
	return acos( sin(x1)*sin(x2) + cos(x1)*cos(x2)*cos(y2-y1) ) * r

def aStar(start, goal):
	frontier = []
	frontier.append((0, start))
	heapq.heapify(frontier)
	path = {}
	cost = {} 
	path[start] = None
	cost[start] = 0
	maxqueue = len(frontier)
	numpop = 0
	while frontier: 
		(cost4now, curr) = heapq.heappop(frontier)
		numpop +=1
		#print curr
		if curr == goal: 
			break
		for neigh in node2neigh[curr]:
			#print neigh
			newcost = cost[curr] + costCalc(curr, neigh)
			if neigh not in cost or newcost < cost[neigh]:
				cost[neigh] = newcost
				pri = newcost + costCalc(goal, neigh)
				#print pri
				frontier.append((pri, neigh))
				if len(frontier) > maxqueue: 
					maxqueue = len(frontier)
				path[neigh] = curr
		heapq.heapify(frontier)
	return (path, cost[goal], maxqueue, numpop)

def dijkstra(start, goal):
	frontier = []
	frontier.append((0, start))
	previous = {}
	cost = {}
	previous[start] = None
	cost[start] = 0 
	maxqueue = len(frontier)
	heapq.heapify(frontier)
	numpop = 0
	while frontier: 
		(costnow, curr) = heapq.heappop(frontier)
		numpop +=1
		if curr == goal: 
			break
		for neigh in node2neigh[curr]:
			altcost = costnow + costCalc(curr, neigh)
			if neigh not in cost or altcost < cost[neigh]:
				cost[neigh] = altcost
				frontier.append((altcost, neigh))
				if len(frontier) > maxqueue: 
					maxqueue = len(frontier)
				previous[neigh] = curr
	return (previous, cost[goal], maxqueue, numpop)

city1 = sys.argv[1]
city2 = sys.argv[2]
if city1 not in city2letter or city2 not in city2letter:
	print "These cities are not in this graph!"

else: 
	(dijDict, cost1, max1, pop1) = dijkstra(city2letter[city1], city2letter[city2])
	pathD = []
	target1 = city2letter[city2]
	while target1 != city2letter[city1]: 
		pathD.append(letter2city[target1])
		target1 = dijDict[target1]
	pathD.append(city1)
	print "Dijkstra Path: "
	print list(reversed(pathD))
	print "Cost: " + str(cost1)
	print "Max queue length: " + str(max1)
	print "Number of nodes popped: " + str(pop1)
	(pathDict, cost2, max2, pop2) = aStar(city2letter[city1], city2letter[city2])
	path = []
	target = city2letter[city2]
	while target != city2letter[city1]: 
		path.append(letter2city[target])
		target = pathDict[target]
	path.append(city1)
	print "-------------------------------"
	print "A Star Path: " 
	print list(reversed(path))
	print "Cost: " + str(cost2)
	print "Max queue length: " + str(max2)
	print "Number of nodes popped: " + str(pop2)


