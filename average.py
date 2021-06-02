def average(statAvg, statThisSession, totalHandsPlayed, handsPlayedThisSession):
	
	newTotal = totalHandsPlayed + handsPlayedThisSession

	weightedAverage = (statThisSession*(handsPlayedThisSession/newTotal)) + (statAvg*(totalHandsPlayed/newTotal))

	return weightedAverage