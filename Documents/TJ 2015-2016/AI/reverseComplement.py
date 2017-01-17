def reverse(string):
	rev = ""
	for i in string: 
		if guard(i):
			if i == 'A':
				rev = rev + 'T'
			elif i  == 'T':
				rev = rev + 'A'
			elif i == 'C':
				rev = rev + 'G'
			elif i == 'G':
				rev = rev + 'C'
		else: 
			rev = rev + i

	return rev


nucset = set(['A', 'T','C', 'G'])

def guard(char):
	if char in nucset:
		return True
	else:
		return False

print reverse("GGATCCGTTCGAAACAGGTT")
