def getID(str):
	# gets FIRST 10 digit ID from string
	i = str.find('@')
	return str[i+2:i+2+10]