import sys, re, math, random
global lateralSwapCount 
def copy(array):
    newarr = []
    for i in range(len(array)):
        newarr.append(array[i])
    return newarr
def findIntersect(board):
    boardarray ={}
    collisions = 0

    for i in range(len(board)):
        col = int(board[i])-1
        row = i
        boardarray[(row,col)] = set()
        hits = set()

        tcol = col+1
        trow = row+1

        while trow<len(board) and tcol<len(board):
            hits.add((trow,tcol))
            trow+=1
            tcol+=1

        tcol = col-1
        trow = row-1

        while trow>=0 and tcol>=0:
            hits.add((trow,tcol))
            trow-=1
            tcol-=1

        tcol = col+1
        trow = row-1

        while tcol<len(board) and trow>=0:
            hits.add((trow,tcol))
            trow-=1
            tcol+=1

        tcol = col-1
        trow = row+1

        while tcol>=0 and trow<len(board):
            hits.add((trow,tcol))
            trow+=1
            tcol-=1

        boardarray[(row,col)] = hits - set([(row,col)])

    moves = boardarray.keys()
    peeped = {}
    for m in moves:
        peeped[m] = set()

    for pos in moves:
        for x in boardarray[pos]:
            if x in moves and x not in peeped[pos]:
                collisions+=1
                peeped[x].add(pos)

    return collisions



def printboard(board):
    lenboard = len(board)
    tstr = ""
    for char in board:
        for i in range(int(char)-1):
            tstr+=("* | ")
        tstr+='q'
        for i in range(lenboard-(int(char))):
            tstr+=(" | *")
        print(tstr)
        xstr = ""
        for i in range(len(tstr)-1):
            xstr+="-"
        print(xstr)
        tstr = ""

def printarray(array):
    for i in ((array)):
        print(i)
    print()

def shuffle(size):
    sizearray = set(range(size))
    lens = len(sizearray)
    board = []
    for i in range(lens):
        rand = random.randint(0,lens)
        while rand not in sizearray:
            rand = random.randint(0,lens)
        sizearray.remove(rand)
        board.append((rand+1))
    return board

def swap(board,r1, r2):
    trow = board[r2]
    board[r2] = board[r1]
    board[r1]  =trow
    return board

def improvepos(board):
    global lateralSwapCount
    tb = copy(board)
    currI = findIntersect(board)
    lateralSwapCount = 0 
    for i in range(len(board)):
        for x in range(len(board)):
            tb = copy(board)
            if not i == x:
                tI = findIntersect(swap(tb,i,x))
                if tI< currI:
                    lateralSwapCount = 0
                    return (i,x)

    return(-1,-1)

def countlateral(board):
    currI = findIntersect(board)
    tb = board
    count = 0
    tcount = 0
    for i in range(len(board)):
        for x in range(len(board)):
            tcount+=1
            tb = board
            if not i == x:
                tI = findIntersect(swap(tb,i,x))
                if tI==currI:
                    count+=1

    return count

def solver(board):
    count = 0
    #print(board)
    #print()
    while(True):
        ximprov, yimprov =  improvepos(board)
        if ximprov == -1:
            print()
            printboard(board)
            return (countlateral(board),count )
        else:
            count+=1
            board = swap(board, ximprov,yimprov)
            #printboard(board)
            #print(board)
            #print()
    return

def finish(board):
    count = 0
    shufflec = 0
    lcount = 0

    while(True):
        if findIntersect(board) == 0:
            lc = 0
            if shufflec >0:
                lc = lcount/shufflec
            return [count,shufflec,lc]
        ximprov, yimprov =  improvepos(board)

        if ximprov == -1:
            shufflec+=1
            board = shuffle(len(board))

        else:
            count+=1
            board = swap(board, ximprov, yimprov)

def Solve():
    n = 100
    for i in range(4,31):
        lp = 0
        c = 0
        sc = 0
        for x in range(n):
            board = shuffle(i)
            array = finish(board)
            lp+= array[2]
            c+=array[0]
            sc+=array[1]
        print(str(i)+": "+str(c/n)+": "+str(sc/n)+": "+str(lp/n))

def Solve1(): 
    board = shuffle(size)
    array = finish(board)
    lp = 0
    c = 0
    sc = 0
    lp+= array[2]
    c+=array[0]
    sc+=array[1]
    print (array)



if len(sys.argv)>1:
    size = int(sys.argv[1])
else:
    size = 3

Solve()
#Solve1()
