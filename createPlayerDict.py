def createPlayerDict():
	# Creates dictionary for poker stats to use to identify players by their nicknames
	# Uses a text file in the folder <playerDictionary.txt>

	playerDict = {}
	f = open('playerDictionary.txt', 'r')

	count = 0
	for line in f:

		line = line.replace('\n', '')
		if count % 2 == 0:       # even lines are keys
			key = line
		else:                    # odd lines are names
			name = line
			playerDict[key] = name
		count += 1

	f.close()

	return playerDict