import numpy as np

def calcPercentAndTranspose(handsPlayed, stat, decimalPlaces):
	# calculate actual statistic over course of hands played per player ------------------------
	

	earlyList = [0] * len(stat[0])
	lateList = [0] * len(stat[0])

	for i in range(len(stat[0])):
		x = handsPlayed[0][i]
		y = handsPlayed[1][i]

		if x == 0:
			earlyList[i] = -1
			lateList[i] =  round(stat[1][i]/handsPlayed[1][i], decimalPlaces)
		elif y == 0:
			earlyList[i] = round(stat[0][i]/handsPlayed[0][i], decimalPlaces)
			lateList[i] =  -1
		else: # x != 0 and y != 0
			earlyList[i] = round(stat[0][i]/handsPlayed[0][i], decimalPlaces)
			lateList[i] =  round(stat[1][i]/handsPlayed[1][i], decimalPlaces)

	totalList = []
	for j in range(len(earlyList)):
		if   x == 0: statTotal = stat[1][j]
		elif y == 0: statTotal = stat[1][j]
		else:        statTotal = stat[0][j] + stat[1][j]

		total = round(statTotal/(handsPlayed[0][j]+handsPlayed[1][j]), decimalPlaces) # calculate average over all positions
		totalList.append(total) # add to overall list

	# Combine position and total lists ----------------------------------------------------------
	tempStat = [[0] * len(stat[0])] * 3 # Create a # players x 3 list (early, late, total)
	
	tempStat[0] = earlyList
	tempStat[1] = lateList
	tempStat[2] = totalList

	numpy_array = np.array(tempStat)
	transpose = numpy_array.T
	statM = transpose.tolist()

	return statM

