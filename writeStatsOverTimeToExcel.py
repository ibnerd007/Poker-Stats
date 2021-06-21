import openpyxl
from search import *
import time

def writeStatsOverTimetoExcel(vpipM, pfrM, tbpM, cbpM, afM, afqM, wtsdM, wasdRelM, mwas, mwbs, 
							  playerIDs, dateFormat, handTypeDesired):
	# Keeps a running bankroll of regular players across multiple sessions
	# Players tracked:
	# Fish, Raymond, Scott, Cedric

	# Read:    playerName = sheet.cell(row=2, column=1).value
	# Write:   sheet.cell(row=i + 2, column=1, value=playerDict[playerIDs[i]])

	""" PLEASE READ: sheet.max_row does not function as expected. Even if there is no value
	in an entire row, those cells can still trigger the max_row object. To reduce max_row, you
	must right click and delete the entire row(s), NOT just the content by pressing 'Delete'.
	Charts and graphs should move up correspondingly; this is how you know you have successfully
	lowered the max_row object. This can cause plenty of errors so be careful when you use it. """

	statsOverTimeIDs = ('L5G0fi1P1T', 'gpL6BdHM3Z', '-4Mt9GCcpf', 'UOl9ieuNTH')
	#                    Fish          Raymond       Scott         Cedric

	# 1. Open workbook and sheet -------------------------------------------------------------

	wb_path = r'Outputs\stats over time.xlsx'

	wb = openpyxl.load_workbook(wb_path) # load existing workbook

	if handTypeDesired == 'NL':
		sheet = wb['NL SOT'] # access sheet
	elif handTypeDesired == 'PLO':
		sheet = wb['PLO SOT'] # access sheet
	else: # combined hand types are desired
		sheet = wb['combined SOT'] # access sheet

	# 2. Check to make sure this session has not already been recorded -----------------------
	#    Compare this session's date with date column

	dates = []
	vpipCols = [3, 13, 23, 33] # columns in Excel where the net will be stored

	for i in range(2, sheet.max_row + 1):
		cellDate = sheet.cell(row=i, column=1).value
		dates.append(cellDate)

	if search(dates, dateFormat) != -1: # data from this date has been entered previously
		# print('Bankroll data not filled... this session already entered\n')
		return
	else: # add date to column
		print('Adding stats over time data...\n')
		if dates == [None]:
			sheet.cell(row=sheet.max_row, column=1, value=dateFormat)
		else:
			sheet.cell(row=sheet.max_row + 1, column=1, value=dateFormat)

	# 3. Add stats for each player -----------------------------------------------

	for i in range(len(statsOverTimeIDs)):

		pI = search(playerIDs, statsOverTimeIDs[i]) # player index
		if pI == -1 and i == 2: # on Scott, search for mobile ID instead
			pI = search(playerIDs, 'X6PyKTwqmn')

		# print('max row =', sheet.max_row)

		playerStats = (vpipM[pI][2], pfrM[pI][2], tbpM[pI][2], afqM[pI][2], 
			wtsdM[pI][2], wasdRelM[pI][2], cbpM[pI][2], afM[pI][2]) # stats are across all positions

		if pI != -1: # player played the session. Else, net remains the same as previously

			for j, stat in enumerate(playerStats):
				# set each stat one by one in a nested loop
				sheet.cell(row=sheet.max_row, column=vpipCols[i] + j, value=stat)
				
				if j != 7: # NOT aggression frequency
					sheet.cell(row=sheet.max_row, column=vpipCols[i] + j).number_format = '0.0%'
				else:
					sheet.cell(row=sheet.max_row, column=vpipCols[i] + j).number_format = '0.00'

		else: # player didn't play this session
			sheet.cell(row=sheet.max_row, column=vpipCols[i] - 1, value='Didn\'t play')
			# Don't fill anything else


	wb.save(wb_path)