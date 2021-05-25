import numpy as np

def calcPercentOfCbpAndTranspose(cbp, decimalPlaces):
	
	earlyList = [0] * len(cbp[0])
	lateList = [0] * len(cbp[0])

	for i in range(len(cbp[0])):
		if cbp[2][i] == 0 and cbp[3][i] == 0: # avoid division by 0
			earlyList[i] = 0 
			lateList[i] =  0		

		elif cbp[2][i] == 0:
			earlyList[i] = 0
			lateList[i] =  round(cbp[1][i]/(cbp[3][i]), decimalPlaces)

		elif cbp[3][i] == 0:
			earlyList[i] = round(cbp[0][i]/(cbp[2][i]), decimalPlaces)
			lateList[i] =  0

		else:
			earlyList[i] = round(cbp[0][i]/(cbp[2][i]), decimalPlaces)
			lateList[i] =  round(cbp[1][i]/(cbp[3][i]), decimalPlaces)

	totalList = []
	for i in range(len(earlyList)):

		if cbp[2][i] == 0 and cbp[3][i] == 0: # avoid division by 0
			total = 0 
		else:
			total = round((cbp[0][i]+cbp[1][i])/(cbp[2][i]+cbp[3][i]), decimalPlaces) # calculate average over all positions

		totalList.append(total) # add to overall list

	# Combine position and total lists ----------------------------------------------------------
	tempcbp = [[0] * len(cbp[0])] * 3 # Create a # players x 3 list (early, late, total)
	
	tempcbp[0] = earlyList
	tempcbp[1] = lateList
	tempcbp[2] = totalList

	numpy_array = np.array(tempcbp)
	transpose = numpy_array.T
	cbpM = transpose.tolist()

	return cbpM

