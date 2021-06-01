def calcAF(af, count, decimals):

	# count[type][position][player]
	# af[position][player]

	# 1. Calculate aggression factor (af) for each player in early and late position
	# AF = (# bets + # raises)/(# calls)
	# actions = ['bets', 'raises', 'calls', 'folds']

	for i in range(len(count[0][0])): # player
		for j in range(len(count[0])): # position

			if count[2][0][i] != 0:
				tempAf = (count[0][j][i] + count[1][j][i])/count[2][j][i] # af = (bets + raises)/calls
			else: # how did they not call once? lol
				tempAf = -1

			af[j][i] = round(tempAf, decimals)

	for k in range(len(count[0][0])): # Number of players
		if   af[0][k] == -1 and af[1][k] == -1: afTotal = 0
		elif af[0][k] == -1:                    afTotal = af[1][k]
		elif af[1][k] == -1:                    afTotal = af[0][k]
		else:                                   afTotal = af[0][k] + af[1][k]

		af[2][k] = round(afTotal/2, decimals)

	return af
