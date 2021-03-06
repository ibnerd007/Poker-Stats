import regex as re

def getNum(str):
	# retrieves the first number without commas (after a 10-digit ID), from string str, 
	# regardless of length
	assert str.find('@') != -1, 'No ID in string'
	afterIDIndex = str.find('@')
	strAfterID = str[afterIDIndex+13:] # Makes sure no numbers in IDs are counted
	# print(strAfterID)

	numRegex = re.findall('[0-9]+', strAfterID)
	assert len(numRegex) >= 1, 'No number in string'
	return int(numRegex[0])