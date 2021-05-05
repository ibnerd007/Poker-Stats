def appendMultiple3D(list, additions):
	# appends multiple indices on end of 3D list
	for i in range(len(list)):
		for j in range(len(list[i])):
			for k in range(additions):
				list[i][j].append(0)
