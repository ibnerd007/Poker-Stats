def addToPlayerDict(id, name):
	# Adds new player and their nickname this session to the dictionary
	# in the correct format

	f = open('playerDictionary.txt', 'a')

	f.write('\n{}'.format(id))
	f.write('\n{}'.format(name))

	f.close()
