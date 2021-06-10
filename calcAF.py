def calcAF(af, count, decimals):

	# count[type][position][player]
	# af[position][player]

	# 1. Calculate aggression factor (af) for each player in early and late position
	# AF = (# bets + # raises)/(# calls)
	# actions = ['bets', 'raises', 'calls', 'folds']

	numPlayers = len(count[0][0])

	for i in range(len(count[0][0])): # player

		# Calculate aggression factor first based on position --------------------------------
		for j in range(len(count[0])): # position

			aggressives = count[0][j][i] + count[1][j][i]
			calls = count[2][j][i]

			if calls != 0:
				tempAf = aggressives/calls
			else: # how did they not call once? lol
				tempAf = -1

			af[j][i] = round(tempAf, decimals)

	# Calculate average aggression factor across all positions -------------------------------
		allAggressives = count[0][0][i] + count[1][0][i] + count[0][1][i] + count[1][1][i]
		#               (early position                )  (late position                  )
		allCalls = count[2][0][i] + count[2][1][i]
		#         (early         ) (late          )

		if allCalls != 0:
			avgTempAf = allAggressives/allCalls
		else: 
			avgTempAf = -1

		af[2][i] = round(avgTempAf, decimals)

	return af
