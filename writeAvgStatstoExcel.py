import openpyxl
from search import *
from average import *

def writeAvgStatstoExcel(vpipM, pfrM, tbpM, cbpCountM, afM, afqM, wtsdM, wasdM, mwas, mwbs, 
  		 			 ledgerM, playerIDs, playerDict, handsPlayed, bestHandsM, date, handTypeDesired):
	# Much like bankrolls, creates a weighted average of stats through total hands played
	# Calculates separately for Holdem and PLO, as well as combined

	# Read:    playerName = sheet.cell(row=2, column=1).value
	# Write:   sheet.cell(row=i + 2, column=1, value=playerDict[playerIDs[i]])

	# 1. Access workbook and correct sheet ----------------------------------------------------------

	wb_path = r'Outputs\stat averages.xlsx'

	wb = openpyxl.load_workbook(wb_path) # load existing workbook

	if handTypeDesired == 'NL':
		sheet = wb['NL Stats-all sessions'] # access sheet
	elif handTypeDesired == 'PLO':
		sheet = wb['PLO Stats-all sessions'] # access sheet
	else: # combined hand types are desired
		sheet = wb['All Stats-all sessions'] # access sheet

	# 2. Establish players of interest, and make sure date is not entered previously ----------------

	statIDs = ['L5G0fi1P1T', 'gpL6BdHM3Z', '-4Mt9GCcpf', 'UOl9ieuNTH']
	#           fish          raymond       scott         cedric

	dates = []

	for i in range(2, sheet.max_row + 1):
		cellDate = sheet.cell(row=i, column=19).value
		dates.append(cellDate)
	# dates is now filled

	print('Dates:', dates)

	if search(dates, date) != -1: # data from this date has been entered previously
		print('Average stat data not filled... this session already entered\n')
		return
	else: # add date to column
		print('Adding average stat data...\n')
		if dates == [None]:
			sheet.cell(row=sheet.max_row, column=1, value=date)
		else:
			sheet.cell(row=sheet.max_row + 1, column=1, value=date)

	# 3. Capturing player indices ------------------------------------------------------------------

	playerIndices = {}

	for ID in statIDs:
		playerIndices[ID] = search(playerIDs, ID)

	# 4. Fill sheet with data

	tdStats = [vpipM, pfrM, tbpM, afqM, wtsdM, wasdM]

	# Fill Excel spreadsheet with percent stat data
	for stat in range(len(tdStats)): # cols
		player = 0
		for ID in playerIndices: # rows
			# Assign player's index this session
			playerIdx = playerIndices[ID]

			if playerIdx != -1:
				# Get stats from this sessiona and averaged sessions
				statAvg = sheet.cell(row=player + 2, column=stat + 3).value
				statThisSession  = tdStats[stat][playerIdx][2]

				# Get hands played this session and total across all sessions
				totalHandsPlayed = sheet.cell(row=player + 2, column=12).value
				handsPlayedThisSession  = handsPlayed[0][playerIdx] + handsPlayed[1][playerIdx]

				# Calculate weighted average
				newStatAvg = average(statAvg, statThisSession, totalHandsPlayed, handsPlayedThisSession)
				
				sheet.cell(row=player + 2, column=stat + 3, value=newStatAvg) # fill percent data
				sheet.cell(row=player + 2, column=stat + 3).number_format = '0.0%'
			
			# Increment for the next row on next loop iteration
			player += 1


	# # Fill Excel spreadsheet with C-bets vs opportunities and aggression factors, not a percent-based stats
	# for player in range(len(playerIDs)): # rows
	# 	sheet.cell(row=player + 2, column=12, value=afM[player][2])
		
	# 	totalBets = cbpCountM[player][0] + cbpCountM[player][1]
	# 	sheet.cell(row=player + 2, column=13, value=totalBets) # fill c-bets

	# 	totalOpps = cbpCountM[player][2] + cbpCountM[player][3]
	# 	sheet.cell(row=player + 2, column=14, value=totalOpps) # fill c-bet opportunities

	player = 0
	for ID in playerIndices:
		playerIdx = playerIndices[ID]

		if playerIdx != -1:

			totalTotal = sheet.cell(row=player + 2, column=12).value

			totalHandsPlayed = handsPlayed[0][playerIdx] + handsPlayed[1][playerIdx]

			sheet.cell(row=player + 2, column=12, value=totalHandsPlayed + totalTotal)
		
		player += 1

	wb.save(wb_path)
