import openpyxl

def writeCurrSessionToExcel(vpipM, pfrM, tbpM, cbpCountM, afM, afqM, wtsdM, wasdM, mwas, mwbs, 
			                ledgerM, playerIDs, playerDict, handsPlayed, bestHandsM, date,
			                handTypeDesired):
	
	# wb = openpyxl.Workbook() # create new workbook
	wb_path = r'Outputs\stats.xlsx'

	wb = openpyxl.load_workbook(wb_path) # load existing workbook

	if handTypeDesired == 'NL':
		sheet = wb['NL Stats-this session'] # access sheet
	elif handTypeDesired == 'PLO':
		sheet = wb['PLO Stats-this session'] # access sheet
	else: # combined hand types are desired
		sheet = wb['All Stats-this session'] # access sheet

	# sheet.insert_rows(1, 2) # Before 1st row, insert 2 columns

	# row = player
	# column = stat index
	# value = stat value

	for i in range(len(playerIDs)): # Fill out player names first
		sheet.cell(row=i + 2, column=1, value=playerDict[playerIDs[i]])

	# Next, fill ledger stats
	for player in range(len(playerIDs)): # cols
		for stat in range(len(ledgerM[0])): # rows
			sheet.cell(row=player + 2, column=stat + 2, value=ledgerM[player][stat]) # averaged positions
			# print(ledgerM[player][stat])

	tdStats = [vpipM, pfrM, tbpM, afM, afqM, wtsdM, wasdM]
	moneyStats = [mwas, mwbs]

	# Fill Excel spreadsheet with percent stat data
	for stat in range(len(tdStats)): # cols
		for player in range(len(playerIDs)): # rows
			sheet.cell(row=player + 2, column=stat + 6, value=tdStats[stat][player][2]) # averaged positions


	# Fill Excel spreadsheet with C-bets vs opportunities, not a percent-based stat
	for player in range(len(playerIDs)): # rows
		totalBets = cbpCountM[player][0] + cbpCountM[player][1]
		sheet.cell(row=player + 2, column=13, value=totalBets) # fill c-bets

		totalOpps = cbpCountM[player][2] + cbpCountM[player][3]
		sheet.cell(row=player + 2, column=14, value=totalOpps) # fill c-bet opportunities


	# Fill Excel spreadsheet with monetary stat data
	for stat in range(len(moneyStats)):
		for player in range(len(playerIDs)):
			sheet.cell(row=player + 2, column=stat + 15, value=moneyStats[stat][player]) # averaged positions

	for player in range(len(playerIDs)):
		totalHandsPlayedPlayed = handsPlayed[0][player] + handsPlayed[1][player]
		sheet.cell(row=player + 2, column=17, value=totalHandsPlayedPlayed) # averaged positions

	row = player + 2 + 1
	rows = sheet.max_row

	sheet.delete_rows(row, sheet.max_row) # delete rows that may remain from previous sessions

	sheet.cell(row=3, column=20, value=date) # date of session

	wb.save(wb_path)




