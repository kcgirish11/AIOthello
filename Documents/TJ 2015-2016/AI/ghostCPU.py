import sys, time, math, string, random
string.ascii_lowercase
ghostList = open("ghost.txt", "r").read().splitlines()
ghostSet = set(ghostList)
for word in ghostList: 
	if len(word) == 3 or len(word) == 2 or len(word) == 1: 
		ghostList.remove(word)
	else:
		for pos in range(len(word)):
			ghostSet.add(word[:pos+1])


		#print word[:pos]
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def checkGhostStatus(curGhost): 
	#print "CURGHOST" + format(curGhost)
	if curGhost == "": 
		return "G"
	elif curGhost == "G": 
		return "GH"
	elif curGhost == "GH": 
		return "GHO"
	elif curGhost == "GHO": 
		return "GHOS"
	elif curGhost == "GHOS":
		return "GHOST"


def playerGhostAdd(playerNum, playerGhost): 
	#print playerGhost[playerNum]
	revGhost = checkGhostStatus(playerGhost[playerNum])
	#print revGhost
	playerGhost[playerNum] = revGhost
	if revGhost == "GHOST":
		return playerNum
	return playerGhost

def possibleSet(word): 
	possSet = set()
	for w in ghostSet:
		if word in w and word != w: 
			#print w.find(word)
			if w.find(word) == 0:
				#print w[len(word)]
				possSet.add(w[len(word)])
	return possSet

getch = _Getch()
numHumPlayers = 0
CPUPlayers = 0
totalPlayers = 0
isPlayerComp = {}
#default is two players, otherwise it is the first argument
if len(sys.argv) == 1:
	for n in range(2): 
		isPlayerComp[n+totalPlayers+1] = False
	numHumPlayers += 2
	totalPlayers += 2
else: 
	for pos in range(1, len(sys.argv)):  
		if sys.argv[pos] == "C": 
			CPUPlayers += 1
			totalPlayers +=1
			isPlayerComp[totalPlayers] = True
		else: 
			#print sys.argv[pos]
			for n in range(int(sys.argv[pos])): 
				isPlayerComp[n+totalPlayers+1] = False
			numHumPlayers += int(sys.argv[pos])
			totalPlayers += int(sys.argv[pos])



print "Human players: " + format(numHumPlayers)
print "CPU players: " + format(CPUPlayers)
totalPlayers = numHumPlayers + CPUPlayers
#print isPlayerComp
roundTrack = 0
playerGhost = {num+1 : "" for num in range(totalPlayers)}
playerTracker = 1
roundTrack = 0
#print isPlayerComp
while roundTrack < 100:
	word = ""
	while "2" not in word:
		if isPlayerComp[playerTracker] == True: 
			if word == "": 
				char = random.choice(string.ascii_lowercase)
				print "CPU Player " + format(playerTracker) + ": " + format(word) + char
			else: 
				choices = possibleSet(word)
				if word in ghostList: 
					char = "#"
					print "CPU Player " + format(playerTracker) + ": " + format(word) + char
					playerGhost = playerGhostAdd(prevPlayer, playerGhost)
					#print playerGhost
					if playerGhost == prevPlayer:
						print "GHOST!!!! GAME OVER Player " + format(prevPlayer) + " lost!"
						quit()
					print "Round over! Player " + format(prevPlayer) + " has " + playerGhost[prevPlayer] + "!"
					word = "2"
				elif not choices: 
					print "CPU Player " + format(playerTracker) + ": " + "This is not a word. I refuse to play with dumbos!"
					quit()
				else:
					#print choices
					char = random.choice(list(choices))
					print "CPU Player " + format(playerTracker) + ": " + format(word) + char
		else:
			print "Player " + format(playerTracker) + ": " + format(word),
			char = getch()
			if char == "*": 
				quit()
			print char
			if char == "#": 
				if word in ghostList: 
					playerGhost = playerGhostAdd(prevPlayer, playerGhost)
					#print playerGhost
					if playerGhost == prevPlayer:
						print "GHOST!!!! GAME OVER Player " + format(prevPlayer) + " lost!"
						quit()
					print "Round over! Player " + format(prevPlayer) + " has " + playerGhost[prevPlayer] + "!"
					word = "2"
				else: 
					playerGhost = playerGhostAdd(playerTracker, playerGhost)
					#print playerGhost
					if playerGhost == playerTracker:
						print "GHOST!!!! GAME OVER Player " + format(playerTracker) + " lost!"
						quit()
					print "Round over! Player " + format(playerTracker) + " has " + playerGhost[playerTracker] + "!"
					word = "2"
			elif char == ".":
				if word in ghostSet:
					print "Possibilites: ", 
					print possibleSet(word)
					char = getch()
					print char
				else: 
					print "NOT IN THE SET"
		word = word + char
		prevPlayer = playerTracker
		playerTracker += 1
		if playerTracker > totalPlayers: 
			playerTracker = 1









