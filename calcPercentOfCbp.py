def calcPercentOfCbp(cbp, decimals):
	
	earlyList = [0] * len(cbp[0])
	lateList = [0] * len(cbp[0])

	for i in range(len(cbp[0])):
		if cbp[2][i] == 0 and cbp[3][i] == 0: # avoid division by 0
			earlyList[i] = 0 
			lateList[i] =  0		

		elif cbp[2][i] == 0:
			earlyList[i] = 0
			lateList[i] =  round(cbp[1][i]/(cbp[3][i]), decimals)

		elif cbp[3][i] == 0:
			earlyList[i] = round(cbp[0][i]/(cbp[2][i]), decimals)
			lateList[i] =  0

		else:
			earlyList[i] = round(cbp[0][i]/(cbp[2][i]), decimals)
			lateList[i] =  round(cbp[1][i]/(cbp[3][i]), decimals)

	totalList = []
	for i in range(len(earlyList)):

		if cbp[2][i] == 0 and cbp[3][i] == 0: # avoid division by 0
			total = 0 
		else:
			total = round((cbp[0][i]+cbp[1][i])/(cbp[2][i]+cbp[3][i]), decimals) # calculate average over all positions

		totalList.append(total) # add to overall list

	# Combine position and total lists ----------------------------------------------------------
	tempCbp = [[0] * len(cbp[0])] * 3 # Create a # players x 3 list (early, late, total)
	
	tempCbp[0] = earlyList
	tempCbp[1] = lateList
	tempCbp[2] = totalList

	return tempCbp

