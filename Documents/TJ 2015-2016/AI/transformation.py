import sys

#showboard
def showBoard(board): 
	print "   ", 
	for l in range(8): 
		print "-",
	print
	for i in range(8): 
		print i,
		print "|",
		for k in range(8):  
			print board[i*8 + k], 
		print "|",
		print i
	print "   ", 
	for l in range(8): 
		print "-",
	print
	print "   ",
	for m in range(8): 
		print m,
	print

#self
def self():
	return range(64)

#rotateLeft 
def rotateLeft(): 
	rlList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrow = col 
			newcol = 7 - row 
			rlList[index] = (8*newrow) + newcol 
	#print rlList
	return rlList

#rotateRight 
def rotateRight(): 
	rrList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrow = 7 - col 
			newcol = row 
			rrList[index] = (8*newrow) + newcol
	return rrList 

#rotate 180
def rotate180(): 
	r180List = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrow = col 
			newcol = 7 - row 
			newrrow = newcol 
			newccol = 7 - newrow
			r180List[index] = (8*newrrow) + newccol 
	return r180List

#flipX 
def flipX(): 
	xList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrrow = 7-row 
			xList[index] = (8*newrrow) + col 
	return xList 

#flipY
def flipY(): 
	yList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newcol = 7-col 
			yList[index] = (8*row) + newcol
	return yList

 
#flip diagnol 
def flipDiagnol(): 
	diagList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 
			newrow = 7-row
			newcol = 7-col 
			diagList[index] = (8*newrow) + newcol
	return diagList

#flip zero
def flipZero(): 
	diagList = [i for i in range(64)]
	for row in range(8): 
		for col in range(8): 
			index = (8*row) + col 	
			if row == col: 
				diagList[index] = index 
			else: 
				diagList[index] = (8*col) + row 
	return diagList



#build dictionary 
def buildTransform(): 
	transformDict = {}
	transformDict['i'] = self()
	transformDict['rl'] = rotateLeft()
	transformDict['rr'] = rotateRight()
	transformDict['r2'] = rotate180()
	transformDict['fx'] = flipX()
	transformDict['fy'] = flipY()
	transformDict['f0'] = flipZero() 
	transformDict['fd'] = flipDiagnol()
	return transformDict


dictTransform = buildTransform()

def transform(technique, puzzle): 
	newindex = dictTransform[technique]
	newboard = ""
	for ind in range(64): 
		newboard = newboard[:ind] + puzzle[newindex[ind]]
	return newboard


testboard = "X........X.......OX......OOXO.....XOO...OOOOO..................."
showBoard(testboard)
while 1: 
	tech = raw_input('Transformation ' )
	if tech == "done": 
		quit()
	newboard = transform(tech, testboard)
	showBoard(newboard)
	print "-----------------------------------"
