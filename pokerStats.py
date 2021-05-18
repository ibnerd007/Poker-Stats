import xlrd
import math

from startingHandNumber import *
from assignPositions import *
from appendMultiple import *
from appendMultiple3D import *
from getID import *
from countAction import *
from resetList import *
from calcPercentAndTranspose import *
from transpose import *
from getNum import *
from numPlayersIn import *
from whichHandType import *
from getPlayerStacks import *

from calcVPIP import *
from calcPFR import *
from calcTBP import *
from calcAF import *
from calcAFQ import *
from calcWTSD import *
from calcWASD import *
from calcMWAS import *
from calcMWBS import *
from calcBestHands import *

from reportPercentages import *
from reportDecimals import *
from printAllStatsForOnePlayer import *
from printAllStatsForAllPlayers import *

from writeCurrSessionToExcel import *
from writeBankrollsToExcel import *

# set date of session & poker type desired (Holdem, PLO, or both)
date = '5 17'
handTypeDesired = 'NL' # can be NL, PLO, or combined
handTypes = ['NL', 'PLO', 'combined']
assert handTypeDesired in handTypes, 'Hand type not recognized'

# Find path to Excel spreadsheet with log and ledger

path_log = "Logs/log_%s.xls" % date
path_ledger = "Ledgers/ledger_%s.xls" % date

log_book = xlrd.open_workbook(path_log)
log_sheet = log_book.sheet_by_index(0)
log_rows = log_sheet.nrows

# Find path to Excel spreadsheet with ledger

ledger_book = xlrd.open_workbook(path_ledger)
ledger_sheet = ledger_book.sheet_by_index(0)
ledger_rows = ledger_sheet.nrows


# The following lists keep track of specific stats; indexed by player ----------------------------------------

# vpip/pfr/tbp = [[fish_early, raymond_early, ...], [fish_late, raymond_late, ...], [fish_alreadyCounted, ...]]
# actionCount = [[[betCount_early_fish, betCount_early_ray,...], [betCount_late_fish, betCount_late_ray]], [callCount_early_fish, callCount_early_ray, ...], ...]
# af = [[af_early_fish, af_early_ray, ...], [af_late_fish, af_late_ray, ...]]
# wtsd = [[wtsd_early_fish, wtsd_early_ray, ...], [wtsd_late_fish, wtsd_late_ray, ...]]
# mwas/mwbs = [money_fish, money_ray, ...]

vpip = [[], [], []] # voluntarily put in pot (%)
pfr  = [[], [], []] # pre flop raise (%)
tbp  = [[], [], []] # 3-bet percentage
actionCount = [[[], []], [[], []], [[], []], [[],[]]] # 3D list that counts every possible action and position when action is made, for each player
													  # to be used for calculating aggression factor and aggression frequency
af = [[], [], []] # 2D list for aggression factor, aggression frequency
afq = [[], [], []] 

wtsd = [[], []] # went to showdown (%)
wasd = [[], []] # won at showdown (%)
mwas = [] # money won at showdown ($)
mwbs = [] # money won before showdown ($) No takers?

# bbWonPerFiftyHands = [] # Big Blinds won per 50 hands

# -----------------------------------------------------------------------------------------------------------

playerIDs = []
handsPlayed = [] # both indexed for each player. Order does not change throughout session.
bestHands = [[], [], [], []] # bestHands = [[hand name (string)], [rank (integer)], [combination (string)], [high card (string)]]
stacks = []

# Static variables
bb = 20 # cents

# Variables changing within while loop
totalPlayed = 0 # total # of hands played
beforeFlop = False
hasRaised = False # there is a raise on the table

holdEm = False
PLO = False # possible hand types
handType = None # set variable used to determine stats for PLO

# Counter for entire log, choose where to start --------------------------------------------------------------
i = 0
counter = 0

while (i < log_rows):
	# Step 1: Parse line beginning with "starting hand #", then 'Player stacks:', then certain actions
	
	str = log_sheet.cell_value(i,0) # get the string for the entire line

	# Preflop -------------------------------------------------------------

	if (str.find('starting hand #') != -1): # row found, indicates starting new hand

		handType = whichHandType(str, handType)

		dealerID = startingHandNumber(str) # dealer ID is determined and returned from this function

		currPlayerIDs = [[], [], []] # ID, seat, position. This is reset every hand
		hasFolded = [] # Tracks who has folded in the hand
		hasCollected = [] # If a player collects a main pot and side pot, they only win at showdown once

		totalPlayed += 1

	# Code must skip every line until it finds a hand that matches desired hand type.
	# This if statement effectively acts like hand types that are not desired were never played
	# if handTypeDesired == 'combined', no problem
	if handType != handTypeDesired and handTypeDesired != 'combined':
		i += 1
		continue

	# Put this if/else after the determination, so only the correct types are presented on the readout
	if str.find('No Limit Texas Hold\'em') != -1: # This hand is NL Holdem
		holdEm = True
	else: # This hand is PLO
		PLO = True


	if (str.find('Player stacks:') != -1): # row found, Players at table are now shown
		assert totalPlayed > 0, "You forgot to run the Excel macro; log order is reversed!"
		playersAdded = assignPositions(str, dealerID, playerIDs, currPlayerIDs, handsPlayed, hasFolded)

		# Add necessary elements to stat lists & counter 3D list to not over-index
		appendMultiple(vpip, playersAdded)
		appendMultiple(pfr, playersAdded) 
		appendMultiple(tbp, playersAdded)
		appendMultiple(af, playersAdded)
		appendMultiple(afq, playersAdded) 
		appendMultiple3D(actionCount, playersAdded) # different function for 3D list
		appendMultiple(wtsd, playersAdded)
		appendMultiple(wasd, playersAdded)
		for j in range(playersAdded): mwas.append(0) # different function for 1D list
		for j in range(playersAdded): mwbs.append(0)
		for j in range(playersAdded): stacks.append(0)

		appendMultiple(bestHands, playersAdded)

		# Get each player's stack based on currPlayerIDs order
		getPlayerStacks(str, stacks, playerIDs, currPlayerIDs)
		print(stacks)
		# writePlayerStacksToExcel(stacks)

		beforeFlop = True

	if str.find('quits the game with a stack of 0') != -1: # a player has busted, change their stack to 0
		bustID = getID(str)
		print(stacks)
		stacks[search(playerIDs, bustID)] = 0 # set their stack to 0 and leave it unless they rejoin

	# Now, look for action preflop: call, raise, and/or 3 bet
	if beforeFlop == True and (str.find('calls') != -1 or str.find('raises') != -1):
		calcVPIP(str, vpip, playerIDs, currPlayerIDs)

		if str.find('raises') != -1: # Looking for a raise preflop
			calcPFR(str, pfr, playerIDs, currPlayerIDs)

			if (hasRaised): # this is now a 3 bet
				calcTBP(str, tbp, playerIDs, currPlayerIDs)
	
			hasRaised = True

	# Flop --------------------------------------------------------------------------------------------

	if str.find('Flop:') != -1: # flop has been shown
		beforeFlop = False
		hasRaised = False
		# reset alreadyCounted lists until next flop
		resetList(vpip[2])
		resetList(pfr[2])
		resetList(tbp[2])
		# break

	# Count the player's action in the actionCount list, regardless whether before flop ---------------
	# This is for the aggression frequency stat

	if str.find('bets') != -1:
		actionID = getID(str)
		countAction(actionID, 'bets', actionCount, currPlayerIDs, playerIDs)

	elif str.find('calls') != -1:
		actionID = getID(str)
		countAction(actionID, 'calls', actionCount, currPlayerIDs, playerIDs)

	elif str.find('raises') != -1:
		actionID = getID(str)
		countAction(actionID, 'raises', actionCount, currPlayerIDs, playerIDs)

	elif str.find('folds') != -1:
		actionID = getID(str)
		countAction(actionID, 'folds', actionCount, currPlayerIDs, playerIDs)
		# Count who has folded for WTSD stat
		hasFolded[search(currPlayerIDs[0], actionID)] = 1 # player has folded


	# End of hand -----------------------------------------------------------------------------------
	# Determine 1) who went to showdown, 2) who won at that showdown, and 3) how much money that player won
	# Store those 3 stats in 3 lists.
	# 1) and 2) are postion-based, 3) is not
	if str.find('collected') != -1 and str.find('combination') != -1: # someone has won the pot at showdown
		winnerID = getID(str)

		# Log who won at showdown
		calcWASD(wasd, winnerID, playerIDs, currPlayerIDs, hasCollected)
		hasCollected.append(winnerID) # player has won and can't win again if a side pot is also collected

		# Collect data for money won at showdown (MWAS)
		pot = getNum(str)
		calcMWAS(mwas, pot, winnerID, playerIDs)

		# Capture the hand they won with IF it is better than the previous best
		wI = search(playerIDs, winnerID) # winner index
		assert wI != -1, 'winner ID not found in playerIDs somehow'
		calcBestHands(str, wI, bestHands)

	elif str.find('collected') != -1: # player has won before showdown. No side pots if there is no showdown (no one is all in)
		winnerID = getID(str)
		pot = getNum(str)
		calcMWBS(mwbs, pot, winnerID, playerIDs)

	if str.find('ending hand #') != -1 and numPlayersIn(hasFolded) >= 2: # Showdown hands only: hand has ended AND two or more players didn't fold
		calcWTSD(wtsd, hasFolded, playerIDs, currPlayerIDs) # All players left went to showdown
			
	i += 1
	print(i)


# Post-loop calculations ------------------------------------------------------------------------------------------
for i in range(len(mwas)): 
	mwas[i] /= 100
	mwbs[i] /= 100 # turn into dollar amounts

# Calculate stat percentages by player in early, late, and total position

vpipM = calcPercentAndTranspose(handsPlayed, vpip, 3)
pfrM = calcPercentAndTranspose(handsPlayed, pfr, 3)
tbpM = calcPercentAndTranspose(handsPlayed, tbp, 4) # Calculates percentages for each preflop statistic
wtsdM = calcPercentAndTranspose(handsPlayed, wtsd, 3)
wasdM = calcPercentAndTranspose(handsPlayed, wasd, 3)

af = calcAF(af, actionCount, 2) # not a percentage
afq = calcAFQ(afq, actionCount, 3) # percentage
afM = transpose(af)
afqM = transpose(afq)

bestHandsM = transpose(bestHands)

# print(playerIDs, '\n')

# ---------------------------------------------------------------------

# ledger = [[total buy-in], [total buy-out], [net profit/loss], [# of rebuys]] per player
ledger = [[], [], [], []]
appendMultiple(ledger, len(playerIDs))
# print(ledger)
cols = {'id': 1, 'buy-in': 4, 'buy-out': 5, 'stack': 6, 'net': 7}

# Loop for ledger
i = 1
while i < ledger_rows:
	# print(cols['buy-in'])
	id = ledger_sheet.cell_value(i, cols['id'])
	idIndex = search(playerIDs,id)
	
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

	i += 1

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

staticIDs = ['L5G0fi1P1T','gpL6BdHM3Z','UOl9ieuNTH','DAovHf6aFe','-4Mt9GCcpf','J_J1Sm6uON',
			 'Tfv9gQlCKp','zQzHYg1f_X','EUC1-Ekcwo','FHfdGMNnXa','UPoeIpvEQ4', 'mZh56-rfJ5',
			 'LragqkH6mQ', 'pnFzv-_qqL', 'jvWHRQaeUN', 'wHCkaNaedp', 'FIgidiXEkn', 'IZfCYGmoLP',
			 'EZvsCiYcdt', 'RlQUK84X1Q', 'F7Ul_O2Igu']
#             fish,        raymond,     cedric,      cheyenne,    scott,       tristan,     
#             kynan,       xavier,      bill,        marshall,    regan,       jonathan,
#			  jacob,       cheyenne,    tristan,     jacob,       jacob,       jacob,
#             Dmkpro67,    colin,       cheyenne

players = ['Fish', 'Raymond', 'Cedric', 'Cheyenne', 'Scott', 'Tristan',
		   'Kynan', 'Xavier', 'Bill', 'Marshall', 'Regan', 'Jonathan', 'Jacob',
		   'Cheyenne', 'Tristan', 'Jacob', 'Jacob', 'Jacob', 'Dmkpro67', 'Colin',
		   'Cheyenne']


playerDict = {'L5G0fi1P1T': 'Fish', 'gpL6BdHM3Z': 'Raymond', 'UOl9ieuNTH': 'Cedric', 

			  'DAovHf6aFe': 'Cheyenne', '-4Mt9GCcpf': 'Scott', 'J_J1Sm6uON': 'Tristan',

		      'Tfv9gQlCKp': 'Kynan', 'zQzHYg1f_X': 'Xavier', 'EUC1-Ekcwo': 'Bill', 

		      'FHfdGMNnXa': 'Marshall', 'UPoeIpvEQ4': 'Regan', 'mZh56-rfJ5': 'Jonathan',

		      'LragqkH6mQ': 'Jacob', 'pnFzv-_qqL': 'Cheyenne', 'jvWHRQaeUN': 'Tristan', 

		      'wHCkaNaedp': 'Jacob', 'FIgidiXEkn': 'Jacob', 'IZfCYGmoLP': 'Jacob', 

		      'EZvsCiYcdt': 'Dmkpro67', 'RlQUK84X1Q': 'Colin', 'F7Ul_O2Igu': 'Cheyenne'}

# -----------------------------------------------------------------------------------------------------------------------
# Now, print everything that should be output:
# 1. List of players
# 2. Date of session
# 3. Statistics & bankroll

print('The following people played this session:')
a = []
for i in range(len(playerIDs)):
	index = search(staticIDs, playerIDs[i])
	if index != -1:
		a.append(players[index])

print(playerIDs, '\n')
print(a, '\n')

print('Date: %s' % date)
assert len(a) == len(playerIDs), 'One or more player IDs are not in dictionary!'

if holdEm == True and PLO == False:
	print('No Limit Texas Hold\'em\n')
elif holdEm == False and PLO == True:
	print('Pot Limit Omaha\n')
else: # both are true, both types were played
	print('No Limit Texas Hold\'em & Pot Limit Omaha\n')

# Call this to see all stats for all players in session ----------------------------

# printAllStatsForAllPlayers(vpipM, pfrM, tbpM, afM, afqM, wtsdM, wasdM, mwas, mwbs, 
# 						   ledgerM, staticIDs, playerIDs, players, handsPlayed, bestHandsM)

# Now, write current session stats for all players to Excel ------------------------

# writeCurrSessionToExcel(vpipM, pfrM, tbpM, afM, afqM, wtsdM, wasdM, mwas, mwbs, 
# 			 ledgerM, staticIDs, playerIDs, playerDict, handsPlayed, bestHandsM, date, handTypeDesired)

# Update the all-time bankrolls for players if not already entered -----------------

# writeBankrollsToExcel(ledgerM, playerIDs, date)

print('Date: ', date)
print('Poker type: ', handTypeDesired, '\n')

