def appendMultiple(list, additions):
	# appends multiple indices on end of 2D list
	for i in range(len(list)):
		list[i] += [0]*additions

