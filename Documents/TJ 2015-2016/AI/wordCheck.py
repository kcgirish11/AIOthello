
def wordDifference(str1, str2):
	diffCheck = False
	if len(str1) == len(str2):
		for i in range (len(str1)):
			if str1[i] != str2[i] and diffCheck == False:
				diffCheck = True
			elif str1[i] != str2[i]:
				return 0
		return 1

	else:
		return -1

print wordDifference("kiran", "biran")
print wordDifference("monkey", "cookie")
print wordDifference("anu", "girish")
print wordDifference("castle", "cattle")
