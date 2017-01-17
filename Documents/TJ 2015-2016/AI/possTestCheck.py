import sys, time, math, string, random
string.ascii_lowercase
ghostList = open("ghost.txt", "r").read().splitlines()
ghostSet = set(ghostList)
def possibleSet(word): 
	possSet = set()
	for w in ghostSet:
		if word in w and word != w: 
			print w.find(word)
			if w.find(word) == 0:
				print w[len(word)]
				possSet.add(w[len(word)])
	return possSet
print possibleSet("gibb")