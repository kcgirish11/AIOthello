#Travelling Salesman
#Kiran Girish 
import sys, math, random, cv2
import numpy as np
distanceDict = {}

file = open("tsp0038.txt", "r")
#reads In the file
def readList(): 
	pointDict = {}
	pointList  = []
	numLines = int(file.readline())
	for l in range(numLines): 
		string = file.readline()
		XY = string.split()
		(x, y) = (float(XY[0]), float(XY[1]))
		pointDict[l+1] = (x, y)
		pointList.append(l+1)
	return (pointList, pointDict)

#calculate cost of the entire tour 
def calculateDistance(pointList, pointDict): 
	totalDist = 0 
	for num in range(len(pointList)): 
		if num < len(pointList) - 1: 
			curPoint = pointList[num]
			nextPoint = pointList[num+1]
		else: 
			curPoint = pointList[num]
			nextPoint = pointList[0]
		(x1, y1) = pointDict[curPoint]
		(x2, y2) = pointDict[nextPoint]
		edgeDist = math.sqrt(((x1-x2)*(x1-x2)) + ((y1 - y2)*(y1-y2)))
		totalDist += edgeDist
	#print (totalDist)
	return totalDist

def distance (cityA, cityB, pointDict): 
	global distanceDict
	if (cityA, cityB) not in distanceDict:
		(x1, y1) = pointDict[cityA]
		(x2, y2) = pointDict[cityB]

#swap in the list 
def swap(pointList, pointDict): 
	curDist = calculateDistance(pointList, pointDict)
	curList = pointList.copy()
	swapCount = 0
	for first in range(len(pointList)): 
		for sec in range(len(pointList)): 
			tempList = pointList.copy()
			temp = tempList[first]
			tempList[first] = tempList[sec]
			tempList[sec] = temp
			dist = calculateDistance(tempList, pointDict)
			#print ("dist", dist)

			if dist < curDist: 
				swapCount += 1
				#print ("here")
				curDist = dist
				curList = tempList.copy()
				break
	#print ("curList", curList)
	#print ("pointList", pointList)
	return (curList, curDist, swapCount)

def reverse(pointList, pointDict): 
	curDist = calculateDistance(pointList, pointDict)
	curList = pointList.copy()
	swapCount = 0
	for first in range(len(pointList)): 
		for sec in range(len(pointList)): 
			tempList = pointList.copy()
			tempList[first:sec] = tempList[first:sec][::-1]
			dist = calculateDistance(tempList, pointDict)
			#print ("dist", dist)
			if dist < curDist: 
				swapCount += 1
				#print ("here")
				curDist = dist
				curList = tempList.copy()
				break
	#print ("curList", curList)
	#print ("pointList", pointList)
	return (curList, curDist, swapCount)

def shuffle(pointList): 
	random.shuffle(pointList)
	#print (pointList)
	return pointList

def drawPic(pointList, pointDict): 
	arr = np.zeros((400,600))
	arr.fill(255)
	pointPicCoord = {}
	
	radius = int(3)
	(x, y) = pointDict[1]
	maxX = x 
	minX = x
	maxY = y 
	minY = y
	for point in pointDict: 
		(x, y) = pointDict[point]
		if x < minX: 
			minX = x 
		elif x > maxX: 
			maxX = x 
		elif y < minY: 
			minY = y
		elif y > maxY: 
			maxY = y 
	rangeX = maxX -  minX
	rangeY = maxY - minY
	print ("rangeX", rangeX)
	print ("rangeY", rangeY)
	proportX = (600 - 150) / rangeX
	proportY =  (400 - 150)/ rangeY
	for point in pointDict: 
		(x, y) = pointDict[point]
		newX = int ((x - minX) * proportX + 100) 
		newY = 400 - int((y - minY) * proportY + 100)
		print ("x", x)
		print ("y", y)
		#print ("newX", newX) 
		#print ("newY", newY)
		cv2.circle(arr, (newX, newY), radius, 0)
		pointPicCoord[point] = (newX, newY)
	for num in range(len(pointList)): 
		if num < len(pointList) - 1: 
			curPoint = pointList[num]
			nextPoint = pointList[num+1]
		else: 
			curPoint = pointList[num]
			nextPoint = pointList[0]
		print ("list", curPoint)
		(x1, y1) = pointPicCoord[curPoint]
		
		(x2, y2) = pointPicCoord[nextPoint]
		cv2.line(arr, (x1, y1), (x2, y2), 0)
	return arr





(pList, pDict) = readList()

pList = [1, 2, 4, 3, 5, 7, 6, 15, 20, 23, 26, 25, 22, 24, 16, 12, 11, 17, 19, 18, 9, 8, 13, 28, 27, 31, 36, 34, 33, 38, 37, 35, 32, 30, 29, 21, 14, 10]
#pic = drawPic(pList, pDict)
while (1): 
	(newList, curDist, sCount) = reverse(pList, pDict)
	if pList == newList: 
		break 
	pList = newList.copy() 

print ("lmao", newList)
newPic = drawPic(newList, pDict)
print ("dist", calculateDistance(pList, pDict))
cv2.imshow('imgWnd', newPic)
cv2.waitKey(0)
cv2.destroyAllWindows()
#print (pDict)
# (order, dist, swapC1) = swap(pList, pDict)
# minDist = dist
# swapCount = swapC1
# #print ("initial MindDist", minDist)
# optList = order.copy() 
# for tri in range(200): 
# 	shuffled = shuffle(pList).copy()
# 	#print ("shuffleCalc", calculateDistance(shuffled, pDict))
# 	newList2 = shuffled.copy()
# 	while (1):  
# 		(newList, distance, swapC) = swap(newList2, pDict)
# 		if newList2 == newList: 
# 			break
# 		newList2 = newList.copy()
# 		swapCount = swapC
# 	#print ("distance", distance)
# 	if distance < minDist:
# 		#print ("sup")
# 		optList = newList.copy() 
# 		minDist = distance 


#print ("MinOrder", optList)
#print ("dist", calculateDistance(optList, pDict))
#print ("distM", minDist)












