import xlrd
import pandas as pd
import time

from startingHandNumber import *
from assignPositions import *
from appendMultiple import *
from appendMultiple3D import *
from getID import *
from getName import *
from countAction import *
from resetList import *
from calcPercentAndTranspose import *
from calcPercentOfCbpAndTranspose import *
from transpose import *
from getNum import *
from numPlayersIn import *
from whichHandType import *
from capturePlayerStacks import *
from addToPlayerDict import *
from createPlayerDict import *

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
from calcCBP import *

from printAllStatsForAllPlayers import *

from writeCurrSessionToExcel import *
from writeBankrollsToExcel import *
from stacksOverTimeLineChart import *
from writeStacksOverTimetoExcel import *
from writeAvgStatstoExcel import *
from whoPlayedWhen import *

def pokerStats(date, handTypeDesired):

	dateFormat = '{}/{}'.format(date[:2], date[2:4])

	handTypes = ['NL', 'PLO', 'combined']
	assert handTypeDesired in handTypes, 'Hand type not recognized'

	# Create dictionary from playerDictionary.txt --------------------------------------------------------------------------

	playerDict = createPlayerDict()

	# ----------------------------------------------------------------------------------------------------------------------

	# Find path to Excel spreadsheet with log and ledger

	path_log = "Logs/log_{}.xls".format(date)
	path_ledger = "Ledgers/ledger_{}.xls".format(date)

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

	cbp = [[], [], [], []] # C-bet %. cbp[[early pos count], [late pos count], [early opportunities count], [late opportunities count]] 

	wtsd = [[], []] # went to showdown (%) by position
	wasd = [[], []] # won at showdown (%)
	mwas = [] # money won at showdown ($)
	mwbs = [] # money won before showdown ($) No takers?

	# -----------------------------------------------------------------------------------------------------------

	# Lists to be filled in loop
	playerIDs = []
	handsPlayed = [[], []] # handsPlayed = [[early], [late]]
	bestHands = [[], [], [], []] # bestHands = [[hand name (string)], [rank (integer)], [combination (string)], [high card (string)]]

	sessionStacks = [] # List that holds stack lists after every hand for every player in session (2D)
	stacks = [] # List that holds stack lists after a single hand for every player in session (1D)

	stackChangeInfo = [] # keeps track of stack add ons or rebuys throughout the session
	bustList = [] # Keeps track of players that are currently busted

	# Variables changing within while loop
	totalPlayed = 0 # total # of hands played
	beforeFlop = False
	hasRaised = False # there is a raise on the table
	beforeTurn = False

	holdEm = False
	PLO = False # possible hand types
	handType = None # set variable used to determine stats for PLO

	aggressorID = None # initalize aggressor ID for program to compare for c-bet statistic

	# Counter for entire log, choose where to start --------------------------------------------------------------
	i = 0

	while (i < log_rows):

		# Step 1: Parse line beginning with "starting hand #", then 'Player stacks:', then certain actions
		
		str = log_sheet.cell_value(i,0) # get the string for the entire line

		# if i == 1 and str.find('requested a seat') == -1:
		# 	raise Exception('Log order is reversed!')

		# Preflop -------------------------------------------------------------

		if str.find('starting hand #') != -1: # row found, indicates starting new hand

			handType = whichHandType(str, handType)

			if not str.find('dead button') != -1: # dead button has NOT been found
				dealerID = startingHandNumber(str) # dealer ID is determined and returned from this function
			else:
				dealerID = 'notAnID' # dummy ID in case there is a dead button on first hand
				# This is possible if someone stands up before the start of the first hand

			currPlayerIDs = [[], [], []] # ID, seat, position. This is reset every hand
			hasFolded = [] # Tracks who has folded in the hand
			hasCollected = [] # If a player collects a main pot and side pot, they only win at showdown once

			totalPlayed += 1

		# Code must skip every line until it finds a hand that matches desired hand type.
		# This if statement effectively acts like hand types that are not desired were never played
		# if handTypeDesired == 'combined', this block is skipped enitrely, and the whole log is processed
		if handType != handTypeDesired and handTypeDesired != 'combined':
			i += 1
			continue

		if handType == 'NL': # This hand is NL Holdem
			holdEm = True
		elif handType == 'PLO': # This hand is PLO
			PLO = True


		# Pre-flop ----------------------------------------------------------------------------------------

		if str.find('Player stacks:') != -1: # row found, Players at table are now shown
			playersAdded = assignPositions(str, dealerID, playerIDs, currPlayerIDs, handsPlayed, hasFolded)

			# if search(currPlayerIDs[0], 'zQzHYg1f_X') != -1: # Xavier is playing
			# 	print('Hand #: ', totalPlayed)
			# 	print('Xavier\'s position: {} \n\n\n'.format(currPlayerIDs[2][search(currPlayerIDs[0], 'zQzHYg1f_X')]))

			# Add necessary elements to stat lists & counter 3D list to not over-index
			appendMultiple(vpip, playersAdded)
			appendMultiple(pfr, playersAdded) 
			appendMultiple(tbp, playersAdded)
			appendMultiple(af, playersAdded)
			appendMultiple(afq, playersAdded) 
			appendMultiple3D(actionCount, playersAdded) # different function for 3D list
			appendMultiple(wtsd, playersAdded)
			appendMultiple(wasd, playersAdded)
			appendMultiple(cbp, playersAdded)
			for j in range(playersAdded): mwas.append(0) # different function for 1D list
			for j in range(playersAdded): mwbs.append(0)
			for j in range(playersAdded): stacks.append(0)

			appendMultiple(bestHands, playersAdded)

			# Get each player's stack based on currPlayerIDs order
			stacks = capturePlayerStacks(str, stacks, playerIDs, currPlayerIDs)
			tempStacks = [item for item in stacks] # 'stacks' points to its old version if appended directly, deepcopy needed
			sessionStacks.append(tempStacks) # will be made into pandas dataframe after loop

			beforeFlop = True

		if str.find('joined') != -1:
			# Player is either:
			# 1. joining the game with his inital stack,
			# 2. rebuying after a bust OR
			# 3. sitting back down after standing up.
			# We need to know which option is happening. ONLY option 2 is applicable here
			joinID = getID(str)

			if joinID in bustList:
				addOnID = joinID
				addOnAmount = getNum(str)
				addOnHand = totalPlayed + 1

				addOnInfo = (addOnID, addOnAmount, addOnHand) # tuple, unchangeable
				stackChangeInfo.append(addOnInfo)

				bustList.remove(addOnID)

		if str.find('quits the game with a stack of 0') != -1: # a player has busted, change their stack to 0
			bustID = getID(str)
			bustIdx = search(playerIDs, bustID)
			
			stacks[bustIdx] = 0 # set their stack to 0 and leave it unless they rejoin

			bustList.append(bustID)

		if str.find('WARNING') != -1 and str.find('adding') != -1: # player is adding on to their stack
			# print('WARNING log message: "{}"\n'.format(str))

			addOnID = getID(str)
			addOnAmount = getNum(str)
			addOnHand = totalPlayed + 1

			addOnInfo = (addOnID, addOnAmount, addOnHand) # tuple, unchangeable
			stackChangeInfo.append(addOnInfo)

		# Look for action throughout the entire hand to add to VPIP
		if str.find('calls') != -1 or str.find('raises') != -1 or str.find('bets') != -1:
			# Find ID of player
			vpipID = getID(str)
			calcVPIP(vpipID, vpip, playerIDs, currPlayerIDs)

			if vpipID not in playerDict:
				name = getName(str, vpipID)
				addToPlayerDict(vpipID, name) # add to text file that keeps a running list of players
				playerDict[vpipID] = name # add new player to this session's dictionary as well

		# Now, look for action preflop: call, raise, and/or 3 bet
		if beforeFlop and str.find('raises') != -1: # Looking for a raise preflop
			calcPFR(str, pfr, playerIDs, currPlayerIDs)

			if hasRaised: # this is now a 3 bet
				calcTBP(str, tbp, playerIDs, currPlayerIDs)

			hasRaised = True

		# Search for pre-flop aggressor for C-bet statistic

		if beforeFlop and str.find('raises') != -1: # raise has been found
			aggressorID = getID(str) # the latest raiser is the aggressor

		# Flop --------------------------------------------------------------------------------------------

		if str.find('Flop:') != -1: # flop has been shown
			beforeFlop = False
			hasRaised = False
			beforeTurn = True
			# reset alreadyCounted lists until next flop
			resetList(pfr[2])
			resetList(tbp[2])

		if beforeTurn and getID(str) == aggressorID and (aggressorID in currPlayerIDs[0]):
			# It is the aggressor's action
			calcCBP(str, cbp, aggressorID, playerIDs, currPlayerIDs) # c-bet percentage

		# Turn --------------------------------------------------------------------------------------------

		if str.find('Turn:') != -1: # turn has been shown
			beforeTurn = False

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

		elif str.find('collected') != -1: 
			# player has won before showdown. No side pots if there is no showdown (no one is all in)
			winnerID = getID(str)
			pot = getNum(str)
			calcMWBS(mwbs, pot, winnerID, playerIDs)

		if str.find('ending hand #') != -1:
			resetList(vpip[2])

			beforeTurn = False

			if numPlayersIn(hasFolded) >= 2: # Showdown hands only: hand has ended AND two or more players didn't fold
				calcWTSD(wtsd, hasFolded, playerIDs, currPlayerIDs) # All players left went to showdown

				
		i += 1

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

	cbpM = calcPercentOfCbpAndTranspose(cbp, 2)
	cbpCountM = transpose(cbp)

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

	cols = {'id': 1, 'buy-in': 4, 'buy-out': 5, 'stack': 6, 'net': 7}

	# Loop for ledger
	i = 1
	while i < ledger_rows:
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

	# -----------------------------------------------------------------------------------------------------------------------
	# Now, print everything that should be output:
	# 1. List of players
	# 2. Date of session
	# 3. Type of poker analyzed (pokerType)
	# 4. Statistics & bankroll

	print('The following people played this session:')
	playerNames = []
	for i in range(len(playerIDs)):
		playerID = playerIDs[i]	
		playerNames.append(playerDict[playerID])

	# print(playerIDs, '\n')
	print(playerNames, '\n')

	whoPlayedWhen(playerNames, playerIDs, dateFormat)

	assert len(playerNames) == len(playerIDs), 'One or more player IDs are not in dictionary!'

	if   holdEm == True  and PLO == False: pokerType = 'No Limit Texas Hold\'em\n'
	elif holdEm == False and PLO == True : pokerType = 'Pot Limit Omaha\n'
	else:                                  pokerType = 'No Limit Texas Hold\'em & Pot Limit Omaha\n'

	print('Date: {}'.format(dateFormat))
	print('Poker type: ', pokerType)
	print('handTypeDesired =', handTypeDesired, '\n')

	if len(playerNames) > 0:
		# Call this to see all stats for all players in session --------------------------------------------------------------------

		printAllStatsForAllPlayers(vpipM, pfrM, tbpM, cbpM, cbpCountM, afM, afqM, wtsdM, wasdM, mwas, mwbs, 
								   ledgerM, playerDict, playerIDs, handsPlayed, bestHandsM)

		# Now, write current session stats for all players to Excel ----------------------------------------------------------------

		writeCurrSessionToExcel(vpipM, pfrM, tbpM, cbpCountM, afM, afqM, wtsdM, wasdM, mwas, mwbs, 
					 			ledgerM, playerIDs, playerDict, handsPlayed, bestHandsM, dateFormat, handTypeDesired)

		# Now, write dataframe containing stack/net data to Excel, then create charts with openpyxl --------------------------------

		writeStacksOverTimetoExcel(sessionStacks, playerNames, stackChangeInfo, playerIDs, handTypeDesired)

		# Update the all-time bankrolls for players if not already entered ---------------------------------------------------------

		# writeBankrollsToExcel(ledgerM, playerIDs, dateFormat)

		# Update the all-time stats for players if not already entered -------------------------------------------------------------

		# writeAvgStatstoExcel(vpipM, pfrM, tbpM, cbpCountM, afM, afqM, wtsdM, wasdM, mwas, mwbs, 
		#   		 		   ledgerM, playerIDs, playerDict, handsPlayed, bestHandsM, date, handTypeDesired)

	else: print('No hands of this type ({}) were played this session.\n'.format(handTypeDesired))

	# --------------------------------------------------------------------------------------------------------------------------

	print('Date: {}'.format(dateFormat))
	print('Poker type: ', pokerType)
	print('handTypeDesired =', handTypeDesired, '\n')
	print('------------------------------------------------------------------------------------------------------')