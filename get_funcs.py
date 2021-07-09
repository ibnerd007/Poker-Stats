import regex as re

def getID(str):
	# gets FIRST 10 digit ID from string
	i = str.find('@')
	return str[i+2:i+2+10]


def getName(str, id):
	# gets name from string before given 10 digit ID
	i = str.find(id)
	assert i != -1, 'ID not contained in string'

	start = str.find('"') + 1
	end = i - 3

	name = str[start:end]

	return name


def getNum(str):
	# retrieves the first number without commas (after a 10-digit ID), from string str, 
	# regardless of length
	assert str.find('@') != -1, 'No ID in string'
	afterIDIndex = str.find('@')
	strAfterID = str[afterIDIndex+13:] # Makes sure no numbers in IDs are counted
	# print(strAfterID)

	numRegex = re.findall('[0-9]+', strAfterID)
	assert len(numRegex) >= 1, 'No number in regex string'

	return int(numRegex[0])