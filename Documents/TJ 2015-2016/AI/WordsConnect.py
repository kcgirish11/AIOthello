#Pranav Gulati 9/8/15 Period 4
import sys, urllib


def checkifRelated(str1, str2):

    if len(str1) != len(str2):
        return -1

    numDiff = 0
    for i in range(0,len(str1)):
        if str1[i] != str2[i]:
            numDiff += 1
            if numDiff > 1:
                return -1
     #Checks to see how manny letters are different
    if numDiff == 1:
        return 1
    else:
        return -1
    #Check if there is a one letter difference in the strings


link = "Words.txt"
hFile = open(link,"r")
wordsArray = []
for line in hFile:
    myWork = line.rstrip("\n")
    wordsArray.append(line)
    #Populates a list of word

listSize = len(wordsArray)
print (listSize)

numedges = 0
for i in range(listSize):
     for x in range(i, listSize, 1):
        if checkifRelated(wordsArray[i], wordsArray[x]) == 1:
            numedges += 1

print(numedges)
