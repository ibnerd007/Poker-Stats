def getName(str, id):
	# gets name from string before given 10 digit ID
	i = str.find(id)
	assert i != -1, 'ID not contained in string'

	start = str.find('"')
	end = i - 3

	name = str[start:end]

	return name

