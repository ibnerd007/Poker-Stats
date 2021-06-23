def calcAF(af, count, decimals):

	# count[type][position][player]
	# af[position][player]

	# 1. Calculate aggression factor (af) for each player in early and late position
	# AF = (# bets + # raises)/(# calls)
	# actions = ['bets', 'raises', 'calls', 'folds']

	positions = len(count[0])
	numPlayers = len(count[0][0])

	for i in range(numPlayers):

		# Calculate aggression factor first based on position ------------------------------------
		for j in range(positions):

			aggressives = count[0][j][i] + count[1][j][i]
			calls = count[2][j][i]

			try:    tempAf = aggressives/calls
			except: tempAf = -1

			af[j][i] = round(tempAf, decimals)


		# Calculate average aggression factor across all positions -------------------------------
		allAggressives = count[0][0][i] + count[1][0][i] + count[0][1][i] + count[1][1][i]
		#               (early position                )  (late position                  )
		allCalls = count[2][0][i] + count[2][1][i]
		#         (early         ) (late          )

		try:    avgTempAf = allAggressives/allCalls
		except: avgTempAf = -1

		af[2][i] = round(avgTempAf, decimals)

	return af
