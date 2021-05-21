import numpy as np

def calcPercentAndTranspose(handsPlayed, stat, decimalPlaces):
	# calculate actual statistic over course of hands played per player ------------------------

	earlyList = [0] * len(stat[0])
	lateList = [0] * len(stat[0])

	for i in range(len(stat[0])):
		earlyList[i] = round(stat[0][i]/(handsPlayed[0][i]), decimalPlaces)
		lateList[i] = round(stat[1][i]/(handsPlayed[1][i]), decimalPlaces)

	totalList = []
	for j in range(len(earlyList)):
		total = round((stat[0][j]+stat[1][j])/(handsPlayed[0][j]+handsPlayed[1][j]), decimalPlaces) # calculate average over all positions
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

