import sys, math, random, time

startTime = time.clock()
#where input = 0 and output = 1
def notFunc1(w, b): 
	output = 1 / (1 + (math.e)** ((-w*(0)) + b))
	return output


#where input = 1 and output = 0
def notFunc2(w, b): 
	output = 1 / (1 + (math.e)** ((-w*(1)) + b))
	return output

def NOT():
	error = math.inf
	w = math.inf
	b = math.inf
	while (error > .00001):
		negative = random.randint(-1,1)
		w = random.random() * (100) * negative
		b = random.random() * 100 * negative
		first = notFunc1(w, b) - 1
		second = notFunc2(w, b) - 0
		error = (first*first) + (second*second)
	print ("Current W", w)
	print ("Current B", b)
	print ("error", error)

def andFunc1(w, b): 
	output = 1 / (1 + (math.e)** (-w*(0+0) + b))
	return output

def andFunc2(w, b): 
	output = 1 / (1 + (math.e)** ((-w*(1+0)) + b))
	return output

def andFunc3(w, b): 
	output = 1 / (1 + (math.e)** ((-w*(0+1)) + b))
	return output

def andFunc4(w, b): 
	output = 1 / (1 + (math.e)** ((-w*(1+1)) + b))
	return output

def AND(): 
	error = math.inf
	w = math.inf
	b = math.inf
	while (error > .00001):
		negative = random.randint(-1,1)
		w = random.random() * (100) * negative
		b = random.random() * 100 * negative
		first = orFunc1(w, b) - 0
		second = orFunc2(w, b) - 1
		third = orFunc2(w, b) - 1
		fourth = orFunc2(w, b) - 1
		error = (first*first) + (second*second) + (third*third) + (fourth*fourth)
	print ("Current W", w)
	print ("Current B", b)
	print ("error", error)

def orFunc1(w, b): 
	output = 1 / (1 + (math.e)** (-w*(0+0) + b))
	return output

def orFunc2(w, b): 
	output = 1 / (1 + (math.e)** ((-w*(1+0)) + b))
	return output

def orFunc3(w, b): 
	output = 1 / (1 + (math.e)** ((-w*(0+1)) + b))
	return output

def orFunc4(w, b): 
	output = 1 / (1 + (math.e)** ((-w*(1+1)) + b))
	return output

def OR(): 
	error = math.inf
	w = math.inf
	b = math.inf
	while (error > .00001):
		negative = random.randint(-1,1)
		w = random.random() * (100) * negative
		b = random.random() * 100 * negative
		first = orFunc1(w, b) - 0
		second = orFunc2(w, b) - 1
		third = orFunc2(w, b) - 1
		fourth = orFunc2(w, b) - 1
		error = (first*first) + (second*second) + (third*third) + (fourth*fourth)
	print ("Current W", w)
	print ("Current B", b)
	print ("error", error)


#NOT()
AND()
#OR()

endTime = (time.clock() - startTime)
print (endTime)






