import time

def calcAFQ(afq, count, decimals):

	# count[type][position][player]
	# afq[position][player]

	# actions = ['bets', 'raises', 'calls', 'folds']

	# Calculate aggression frequency (afq) for each player in early and late position
	# AFQ = (bets + raises)/(bets + raises + calls + folds)

	for i in range(len(count[0][0])): # player
		for j in range(len(count[0])): # position

			# Calculate aggression factor first based on position --------------------------------
			totalCount = count[0][j][i] + count[1][j][i] + count[2][j][i] + count[3][j][i]
			aggressives = count[0][j][i] + count[1][j][i]

			if totalCount != 0:
				tempAFQ = aggressives/totalCount
			else:
				tempAFQ = -1

			afq[j][i] = round(tempAFQ, decimals)

	# Calculate average aggression frequency across both positions -------------------------------
		allAggressives = count[0][0][i] + count[1][0][i] + count[0][1][i] + count[1][1][i]

		allTotalCount = count[0][0][i] + count[1][0][i] + count[2][0][i] + count[3][0][i] + \
						 count[0][1][i] + count[1][1][i] + count[2][1][i] + count[3][1][i]

		avgTempAfq = allAggressives/allTotalCount

		afq[2][i] = round(avgTempAfq, decimals)

	return afq

