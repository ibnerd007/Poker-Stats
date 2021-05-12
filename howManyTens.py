def howManyTens(str):
	tens = 0

	while str.find('10') != -1: # tens are still lurking
		tens += 1
		str = str[str.find('10') + 2:]

	return tens