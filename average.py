def average(statAvg, statThisSession, totalHandsPlayed, handsPlayedThisSession):
	
	newTotal = totalHandsPlayed + handsPlayedThisSession # total hands played over previous sessions and
														 # this session combined

	weightedAverage = (statThisSession*(handsPlayedThisSession/newTotal)) + (statAvg*(totalHandsPlayed/newTotal))

	return weightedAverage