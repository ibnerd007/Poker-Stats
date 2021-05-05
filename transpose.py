import numpy as np

def transpose(list):
	numpy_array = np.array(list)
	transpose = numpy_array.T
	Tlist = transpose.tolist()

	return Tlist