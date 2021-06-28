def whoPlayedWhen(names, IDs, date):
	# Stores player nicknames and IDs into a text file
	# This will help reference who played what session as there are more sessions
	path = r'Outputs\whoPlayedWhen.txt'

	f = open(path, 'r')

	prevDates = []

	for (i, line) in enumerate(f):
		if 'Date: ' in line:
			line = line.replace('\n', '')
			prevDates.append(line[6:]) # Text past 'Date: '

	f.close()

	# --------------------------------------------------------------------------

	f = open(path, 'a')

	if date not in prevDates:
		print('Storing names and IDs for this session...')

		line1 = ('Date: ', date, '\n')
		
		f.writelines(line1)

		for (i, ID) in enumerate(IDs):
			f.write(ID)
			f.write('     ')
			f.write(names[i])
			f.write('\n')

		f.write('\n')

	f.close()