import xlrd
from appendMultiple import *
from transpose import *
from search import *

def calcLedger(path, playerIDs):
	# Find path to Excel spreadsheet with ledger

	ledger_book = xlrd.open_workbook(path)
	ledger_sheet = ledger_book.sheet_by_index(0)
	ledger_rows = ledger_sheet.nrows

	# ledger = [[total buy-in], [total buy-out], [net profit/loss], [# of rebuys]] per player
	ledger = [[], [], [], []]
	appendMultiple(ledger, len(playerIDs))

	cols = {'id': 1, 'buy-in': 4, 'buy-out': 5, 'stack': 6, 'net': 7}

	# Loop for ledger -----------------------------------------------------------------------

	for i in range(1, ledger_rows):

		id = ledger_sheet.cell_value(i, cols['id'])
		idIndex = search(playerIDs, id)
		
		if idIndex == -1: # player did not play this type, but is still in the ledger
		# Still print their ledger stats for the session
			i += 1
			continue

		# Capture the player's buy in so far
		buyIn = ledger_sheet.cell_value(i, cols['buy-in'])
		ledger[0][idIndex] += buyIn

		# Capture the player's buy out
		buyOut = ledger_sheet.cell_value(i, cols['buy-out'])

		if buyOut != '': # player 'left' the table
			ledger[1][idIndex] += buyOut
		else: # player never technically 'left' so still has a 'stack'
			ledger[1][idIndex] += ledger_sheet.cell_value(i, cols['stack'])

		# Catpure the player's net profit/loss
		net = ledger_sheet.cell_value(i, cols['net'])
		ledger[2][idIndex] += net

		# Capture the player's rebuys
		ledger[3][idIndex] += 1

	for i in range(len(playerIDs)): ledger[3][i] -= 1 # Correct # of rebuys

	ledgerM = transpose(ledger)

	# Make into dollar amounts and round to necessary digits
	for i in range(len(playerIDs)):
		for j in range(len(ledgerM[0])):
			if j < 3: # monetary amounts, not # of rebuys
				ledgerM[i][j] /= 100
				ledgerM[i][j] = round(ledgerM[i][j], 2) # $ amounts are in cents
			else:
				ledgerM[i][j] = round(ledgerM[i][j]) # number of rebuys is an integer

	# -------------------------------------------------------------------------------------

	return ledgerM