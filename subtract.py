def subtract(minuend, subtrahend):
	# Subtracts two lists: the subtrahend from the minuend
	
	assert len(minuend) == len(subtrahend), 'Lists cannot be subtracted: are different lengths'

	difference = [0] * len(minuend)

	for i in range(len(minuend)):
		difference[i] = minuend[i] - subtrahend[i]
		difference[i] = round(difference[i], 2)

	return difference

