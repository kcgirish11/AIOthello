import sys, time, math
ghostList = open("ghost.txt", "r").read().splitlines()
ghostSet = set(ghostList)
for word in ghostList: 
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
			if w.find(word) == 0:
				#print w
				pos = w.find(word[len(word)-1])
				possSet.add(w[pos+1])
	return possSet


getch = _Getch()
numPlayers = 0
#default is two players, otherwise it is the first argument
if len(sys.argv) == 1:
	numPlayers = 2
else: 
	numPlayers = int(sys.argv[1])
print "Human players: " + format(numPlayers)
roundTrack = 0
playerGhost = {num+1 : "" for num in range(numPlayers)}
while roundTrack < 5: 
	word = ""
	playerTracker = 1 
	while "2" not in word:
		print "Player " + format(playerTracker) + ": " + format(word),
		char = getch()
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
				"NOT IN THE SET"
		word = word + char
		prevPlayer = playerTracker
		playerTracker += 1
		if playerTracker > numPlayers: 
			playerTracker = 1








