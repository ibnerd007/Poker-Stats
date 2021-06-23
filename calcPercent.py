def calcPercent(statCount, totalCount, decimals):
	# calculate actual statistic over course of hands played per player ------------------------
	
	numPlayers = len(statCount[0])

	earlyList = [0] * numPlayers
	lateList = [0] * numPlayers

	totalList =[] # for temporarily holding average stats across positions

	for i in range(numPlayers):
		x = totalCount[0][i]
		y = totalCount[1][i]

		try:    earlyList[i] = round(statCount[0][i]/x, decimals)
		except: earlyList[i] = 0

		try:    lateList[i] =  round(statCount[1][i]/y, decimals)
		except: lateList[i] =  0

		# Calculate stat averages now across both positions

		statTotal = statCount[0][i] + statCount[1][i]
		totalPlayed = totalCount[0][i] + totalCount[1][i]

		try:    total = round(statTotal/totalPlayed, decimals) # calculate average over all positions
		except: total = 0
			
		totalList.append(total) # add to overall list

	# Combine position and total lists ----------------------------------------------------------
	stat = [[0] * numPlayers] * 3 # Create a # players x 3 list (early, late, total)
	
	stat[0] = earlyList
	stat[1] = lateList
	stat[2] = totalList

	return stat

