def subtract(minuend, subtrahend):
	# Subtracts two lists: the subtrahend from the minuend
	
	assert len(minuend) == len(subtrahend), 'Lists cannot be subtracted: are different lengths'

	length = len(minuend)

	difference = [0] * length

	for i in range(length):
		difference[i] = minuend[i] - subtrahend[i]
		difference[i] = round(difference[i], 2)

	return difference

