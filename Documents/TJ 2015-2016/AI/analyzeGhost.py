import sys, time, math, string, random
string.ascii_lowercase
ghostList = open("ghost.txt", "r").read().splitlines()
ghostSet = set(ghostList)
for word in ghostList:
	if len(word) <= 3: 
		ghostSet.remove(word)

def possibleSet(word): 
	possSet = set()
	for w in ghostSet:
			if word in w and word != w: 
				#print w.find(word)
				if w.find(word) == 0:
					#print w[len(word)]
					possSet.add(w[len(word)])
	return possSet

def analyze(prefix, playerNum): 
	if prefix in ghostSet: 
		return ({prefix}, set())
	(good,bad) = (set(),set())
	for pos in possibleSet(prefix):
		tempGood, tempBad = analyze(prefix + pos, 1-playerNum)
		if not tempGood: 
			good.add(pos)
		else: 
			bad.add(pos)
	return (good,bad)

def buildTrie(prefix, wordIt): 
	myDct = {}
	for word in wordIt: 
		if len(word) < 4: continue
		

pref = sys.argv[1]
print analyze(pref, 1) 


