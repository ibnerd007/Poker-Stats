import numpy as np

def calcPercentAndTranspose(handsPlayed, statCount, decimalPlaces):
	# calculate actual statistic over course of hands played per player ------------------------
	
	numPlayers = len(statCount[0])

	earlyList = [0] * numPlayers
	lateList = [0] * numPlayers

	for i in range(numPlayers):
		x = handsPlayed[0][i]
		y = handsPlayed[1][i]

		if x == 0 and y != 0: 
			# no early position hands played
			earlyList[i] = -1
			lateList[i] =  round(statCount[1][i]/handsPlayed[1][i], decimalPlaces)

		elif y == 0 and x != 0: 
			# no late position hands played
			earlyList[i] = round(statCount[0][i]/handsPlayed[0][i], decimalPlaces)
			lateList[i] =  -1

		elif y == 0 and x == 0:
			earlyList[i] = -1
			lateList[i] =  -1

		else: 
			# hands played in both positions
			earlyList[i] = round(statCount[0][i]/handsPlayed[0][i], decimalPlaces)
			lateList[i] =  round(statCount[1][i]/handsPlayed[1][i], decimalPlaces)

	totalList = []
	for j in range(numPlayers):
		if   x == 0: statTotal = statCount[1][j]
		elif y == 0: statTotal = statCount[1][j]
		else:        statTotal = statCount[0][j] + statCount[1][j]

		totalPlayed = handsPlayed[0][j] + handsPlayed[1][j]
		if totalPlayed != 0:
			total = round(statTotal/(handsPlayed[0][j]+handsPlayed[1][j]), decimalPlaces) # calculate average over all positions
		else: 
			total = -1
			
		totalList.append(total) # add to overall list

	# Combine position and total lists ----------------------------------------------------------
	tempStat = [[0] * numPlayers] * 3 # Create a # players x 3 list (early, late, total)
	
	tempStat[0] = earlyList
	tempStat[1] = lateList
	tempStat[2] = totalList

	numpy_array = np.array(tempStat)
	transpose = numpy_array.T
	statM = transpose.tolist()

	return statM

