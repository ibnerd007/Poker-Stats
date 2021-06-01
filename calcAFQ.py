import time

def calcAFQ(afq, count, decimals):

	# count[type][position][player]
	# afq[position][player]

	# actions = ['bets', 'raises', 'calls', 'folds']

	# Calculate aggression frequency (afq) for each player in early and late position
	# AFQ = (bets + raises)/(bets + raises + calls + folds)

	for i in range(len(count[0][0])): # player
		for j in range(len(count[0])): # position

			totalCount = count[0][j][i] + count[1][j][i] + count[2][j][i] + count[3][j][i]

			if totalCount != 0:
				tempAFQ = (count[0][j][i] + count[1][j][i])/totalCount
			else:
				tempAFQ = -1

			afq[j][i] = round(tempAFQ, decimals)

	# Calculate average aggression frequency across both positions

	for k in range(len(count[0][0])): # Number of players
		if   afq[0][k] == -1: afqTotal = afq[1][k]
		elif afq[1][k] == -1: afqTotal = afq[0][k]
		else:                 afqTotal = afq[0][k] + afq[1][k]

		afq[2][k] = round(afqTotal/2, decimals)

	print(afq)

	return afq

