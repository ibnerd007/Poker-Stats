def calcAF(af, count, decimals):

	# count[type][position][player]
	# af[position][player]

	# 1. Calculate aggression factor (af) for each player in early and late position
	# AF = (# bets + # raises)/(# calls)
	# actions = ['bets', 'raises', 'calls', 'folds']

	for i in range(len(count[0][0])): # player
		for j in range(len(count[0])): # position

			if (count[2][0][i] != 0):
				tempAf = (count[0][j][i] + count[1][j][i])/count[2][j][i] # af = (bets + raises)/calls
			else: # how did they not call once? lol
				tempAf = -1

			af[j][i] = round(tempAf, decimals)

	for k in range(len(count[0][0])): # Number of players
		af[2][k] = round((af[0][k] + af[1][k])/2, decimals)

	return af
