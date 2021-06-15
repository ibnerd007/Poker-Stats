import openpyxl
from search import *

def writeBankrollsToExcel(ledgerM, playerIDs, dateFormat):
	# Keeps a running bankroll of regular players across multiple sessions
	# Players tracked:
	# Fish, Raymond, Scott, Cedric, Cheyenne, Tristan

	# Read:    playerName = sheet.cell(row=2, column=1).value
	# Write:   sheet.cell(row=i + 2, column=1, value=playerDict[playerIDs[i]])

	bankrollIDs = ('L5G0fi1P1T', 'gpL6BdHM3Z', '-4Mt9GCcpf', 'UOl9ieuNTH', 'DAovHf6aFe')
	#               Fish          Raymond       Scott         Cedric        Cheyenne

	# 1. Open workbook and sheet

	wb_path = r'Outputs\bankrolls.xlsx'

	wb = openpyxl.load_workbook(wb_path) # load existing workbook

	sheet = wb['Bankrolls'] # access sheet

	# 2. Check to make sure this session has not already been recorded
	#    Compare this session's date with date column

	dates = []
	netCols = [3, 8, 13, 18, 23] # columns in Excel where the net will be stored

	# print('Max row: ', sheet.max_row)

	for i in range(2, sheet.max_row + 1):
		cellDate = sheet.cell(row=i, column=1).value
		dates.append(cellDate)

	if search(dates, dateFormat) != -1: # data from this date has been entered previously
		print('Bankroll data not filled... this session already entered\n')
		return
	else: # add date to column
		print('Adding bankroll data...\n')
		if dates == [None]:
			sheet.cell(row=sheet.max_row, column=1, value=dateFormat)
		else:
			sheet.cell(row=sheet.max_row + 1, column=1, value=dateFormat)

	# 3. Add net to current net for each player -----------------------------------------------

	for i in range(len(bankrollIDs)):
		index = search(playerIDs, bankrollIDs[i])
		if index == -1 and i == 4: # on Cheyenne, search for alternate ID
			index = search(playerIDs, 'pnFzv-_qqL')
		if index == -1 and i == 2: # on Scott, search for mobile ID instead
			index = search(playerIDs, 'X6PyKTwqmn') 

		newNet = sheet.cell(row=sheet.max_row-1, column=netCols[i]).value

		if index != -1: # player played the session. Else, net remains the same as previously
			newNet += ledgerM[index][2]

			bankroll = sheet.cell(row=sheet.max_row-1, column=netCols[i] + 1).value
			ownMoneyInvested = sheet.cell(row=sheet.max_row-1, column=netCols[i] + 2).value
			buyIn = ledgerM[index][0]

			if buyIn > bankroll:
				ownMoneyInvested += (buyIn - bankroll)
				bankroll += (buyIn - bankroll) # update bankroll if more money was added to play

			net = ledgerM[index][2] # just set above

			bankroll += net

			assert bankroll >= 0, 'Bankroll = %.2f < 0: %s' % (bankroll, bankrollIDs[i])

			sheet.cell(row=sheet.max_row, column=netCols[i], value=newNet)
			sheet.cell(row=sheet.max_row, column=netCols[i] + 1, value=bankroll) # set bankroll
			sheet.cell(row=sheet.max_row, column=netCols[i] + 2, value=ownMoneyInvested) # set own money invested


		else: # show that player didn't play and fill columns

			UNCHnet              = sheet.cell(row=sheet.max_row-1, column=netCols[i]).value
			UNCHbankroll         = sheet.cell(row=sheet.max_row-1, column=netCols[i] + 1).value
			UNCHownMoneyInvested = sheet.cell(row=sheet.max_row-1, column=netCols[i] + 2).value

			sheet.cell(row=sheet.max_row, column=netCols[i] - 1, value='Didn\'t play')
			sheet.cell(row=sheet.max_row, column=netCols[i], value=UNCHnet)
			sheet.cell(row=sheet.max_row, column=netCols[i] + 1, value=UNCHbankroll) # set bankroll
			sheet.cell(row=sheet.max_row, column=netCols[i] + 2, value=UNCHownMoneyInvested) # all values are unchanged from previous


	wb.save(wb_path)