def appendMultiple(list, additions):
	# appends multiple indices on end of 2D list
	for i in range(len(list)):
		for j in range(additions):
			list[i].append(0)

