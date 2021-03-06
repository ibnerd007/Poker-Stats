import xlrd, time, copy
import pandas as pd

from assignDealer import *
from assignPositions import *
from appendMultiple import *
from appendMultiple3D import *
from countAction import *
from resetList import *
from calcPercent import *
from transpose import *
from numPlayersIn import *
from whichHandType import *
from capturePlayerStacks import *
from createPlayerDict import *
from assignPlayerIndices import *

from getID import *
from getName import *
from getNum import *

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
from calcLedger import *

from printAllStatsForAllPlayers import *
from writeCurrSessionToExcel import *
from writeBankrollsToExcel import *
from stacksOverTimeLineChart import *
from writeStacksOverTimetoExcel import *
from writeStatsOverTimeToExcel import *
from writeAvgStatstoExcel import *
from whoPlayedWhen import *
from addToPlayerDict import *
from wipeCurrSessionSheets import *


def pokerStats(date, handTypeDesired, includeCMD):

	dateFormat = '{}/{}/{}'.format(date[:2], date[2:4], date[4:])

	# handTypesPossible = ['NL', 'PLO', 'combined']

	# Create dictionary from playerDictionary.txt ----------------------------------------------------------------

	playerDict = createPlayerDict()

	# ------------------------------------------------------------------------------------------------------------

	# Find path to Excel spreadsheet with log and ledger

	path_log = "Logs/log_{}.xls".format(date)

	log_book = xlrd.open_workbook(path_log)
	log_sheet = log_book.sheet_by_index(0)
	log_rows = log_sheet.nrows

	# The following lists keep track of specific stats; indexed by player ----------------------------------------

	# vpip/pfr/tbp = [[fish_early, raymond_early, ...], [fish_late, raymond_late, ...], [fish_alreadyCounted, ...]]

	# actionCount = [[[betCount_early_fish, betCount_early_ray,...], [betCount_late_fish, betCount_late_ray]], 
	#				  [callCount_early_fish, callCount_early_ray, ...], ...]

	# af = [[af_early_fish, af_early_ray, ...], [af_late_fish, af_late_ray, ...]]

	# wtsd = [[wtsd_early_fish, wtsd_early_ray, ...], [wtsd_late_fish, wtsd_late_ray, ...]]

	# mwas/mwbs = [money_fish, money_ray, ...]

	vpip = [[], [], []] # voluntarily put in pot (%)
	pfr  = [[], [], []] # pre flop raise (%)
	tbp  = [[], [], []] # 3-bet percentage
	actionCount = [[[], []], [[], []], [[], []], [[],[]]] # 3D list that counts every possible action and position when action is made, 
														  # for each player to be used for calculating aggression factor and aggression 
														  # frequency
	af = [[], [], []] # 2D list for aggression factor, aggression frequency
	afq = [[], [], []]

	cbp = [[], [], [], []] # C-bet %. cbp[[early pos count], [late pos count], [early opportunities count], [late opportunities count]] 

	wtsd = [[], []] # went to showdown (%) by position
	wasd = [[], []] # won at showdown (%) by position
	mwas = [] # money won at showdown ($)
	mwbs = [] # money won before showdown ($) No takers?

	# -----------------------------------------------------------------------------------------------------------

	# Lists to be filled in loop
	playerIDs = [] # Keeps every player's session ID in the order in which they arrived
	handsPlayed = [[], []] # handsPlayed = [[early], [late]]
	bestHands = [[], [], [], []] # bestHands = [[hand name (string)], [rank (integer)], [combination (string)], [high card (string)]]

	sessionStacks = [] # List that holds stack lists after every hand for every player in session (2D)
	stacks = [] # List that holds stack lists after a single hand for every player in session (1D)

	stackChangeInfo = [] # keeps track of stack add ons or rebuys throughout the session
	bustList = [] # Keeps track of players that are currently busted

	# Variables changing within while loop
	totalPlayed = 0 # total # of hands played
	beforeFlop = False
	beforeTurn = False

	hasRaised = False # there is a raise on the table

	holdEm = False
	PLO = False # possible hand types
	handType = None # set variable used to determine stats for PLO

	aggressorID = None # initalize aggressor ID for program to compare for c-bet statistic

	# Main loop, beginning at either beginning or end -------------------------------------------------------

	# If loop should be from the beginning, add to this tuple of dates in Excel where log order is already
	# switched.

	debugDates = ('040921','041621','041921','042421','042621','042921','050421','051321','051721',
				  '052021','052421','052721','052821','053121','060721','061021','061421','061521',
				  '061721','062121','062421')

	if path_log[9:15] in debugDates: # run from top to bottom of log for debugging purposes
		begin = 0
		end = log_rows
		order = 1
	else: 
		begin = log_rows-1
		end = 0 # will not include entry row
		order = -1

	# ---------------------------------------------------------------------------------------------------------

	for i in range(begin, end, order):

		# Step 1: Parse line beginning with "starting hand #", then 'Player stacks:', then certain actions
		
		str = log_sheet.cell_value(i,0) # get the string for the entire line

		# Preflop -------------------------------------------------------------

		if str.find('starting hand #') != -1: # row found, indicates starting new hand

			if totalPlayed == 0: # very first hand seen
				index = str.find('starting hand #')
				handNum = str[index+15:index+15+3]

				if handNum != '1  ':
					raise Exception('Log order is incorrect, expected hand 1, got {}'.format(handNum))

			handType = whichHandType(str, handType)

			if not str.find('dead button') != -1: # dead button has NOT been found
				dealerID = assignDealer(str) # dealer ID is determined and returned from this function
			else:
				dealerID = 'notAnID' # dummy ID in case there is a dead button on first hand
				# This is possible if someone stands up before the start of the first hand
				# For the first hand, penultimate player will be the dealer

			currPlayerIDs = [[], [], []] # ID, seat, position. This is reset every hand
			hasFolded = [] # Tracks who has folded in the hand
			hasCollected = [] # Track who has already collected from pot.
							  # If a player collects a main pot and side pot, they only win at showdown once

			totalPlayed += 1

		# Code must skip every line until it finds a hand that matches desired hand type.
		# This if statement effectively acts like hand types that are not desired were never played
		# if handTypeDesired == 'combined', this block is skipped enitrely, and the whole log is processed
		if handType != handTypeDesired and handTypeDesired != 'combined': continue

		if handType == 'NL': # This hand is NL Holdem
			holdEm = True
		elif handType == 'PLO': # This hand is PLO
			PLO = True


		# Pre-flop ----------------------------------------------------------------------------------------

		if str.find('Player stacks:') != -1: # row found, Players at table are now shown
			playersAdded = assignPositions(str, dealerID, playerIDs, currPlayerIDs, handsPlayed, hasFolded)

			# Add necessary elements to stat lists
			# 1-D
			mwas   += [0]*playersAdded
			mwbs   += [0]*playersAdded
			stacks += [0]*playersAdded

			# 2-D
			appendMultiple(vpip, playersAdded)
			appendMultiple(pfr, playersAdded) 
			appendMultiple(tbp, playersAdded)
			appendMultiple(af, playersAdded)
			appendMultiple(afq, playersAdded) 
			appendMultiple(wtsd, playersAdded)
			appendMultiple(wasd, playersAdded)
			appendMultiple(cbp, playersAdded)
			appendMultiple(bestHands, playersAdded)

			# 3-D
			appendMultiple3D(actionCount, playersAdded) # different function for 3D list

			# Get each player's stack based on currPlayerIDs order
			stacks = capturePlayerStacks(str, stacks, playerIDs, currPlayerIDs)
			sessionStacks.append(copy.deepcopy(stacks)) # will be made into pandas dataframe after loop

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
				
				isReset = False 
				""" Stack is not being reset to a new value; 
				player is buying back in (effectively adding on) """

				addOnInfo = (addOnID, addOnAmount, addOnHand, isReset)
				stackChangeInfo.append(addOnInfo)

				bustList.remove(addOnID)

		if str.find('quits the game with a stack of 0') != -1: # a player has busted
			bustID = getID(str)
			bustIdx = search(playerIDs, bustID)
			
			stacks[bustIdx] = 0 # set their stack to 0 and leave it unless they rejoin

			bustList.append(bustID)

		if str.find('WARNING') != -1 and totalPlayed > 0: # player hasn't busted, but wants to add chips
			""" It is possible to change stack before the first hand, but these situations must
			be ignored because they cause issues when calculating net stacks, and they don't represent
			actual changes in a player's net gain/loss. """
			addOnID = getID(str)
			amount = getNum(str)
			addOnHand = totalPlayed + 1

			if str.find('adding') != -1: # player is adding on to their stack
				isReset = False
				addOnInfo = (addOnID, amount, addOnHand, isReset)
				stackChangeInfo.append(addOnInfo)

			elif str.find('reseting') != -1: # player is resetting their stack to a certain amount
				isReset = True
				addOnInfo = (addOnID, amount, addOnHand, isReset)
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

			pfrID = getID(str)
			calcPFR(pfrID, pfr, playerIDs, currPlayerIDs)

			if hasRaised: # this is now a 3 bet

				tbID = getID(str)
				calcTBP(tbID, tbp, playerIDs, currPlayerIDs)
				# Note: Every 4-bettor, 5-bettor, and onwards will also be counted in TBP stat.

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
			beforeFlop = False # in case there is no flop or turn, these parameters still reset
			hasRaised = False # in case hasRaised is tripped and there is no flop, it is also reset

			if numPlayersIn(hasFolded) >= 2: # Showdown hands only: hand has ended AND two or more players didn't fold
				calcWTSD(wtsd, hasFolded, playerIDs, currPlayerIDs) # All players left went to showdown

	# Post-loop calculations ------------------------------------------------------------------------------------------
	for i in range(len(mwas)): 
		mwas[i] /= 100
		mwbs[i] /= 100 # turn into dollar amounts

	# Calculate stat percentages by player in early, late, and total position
	# statM is indexed: statM[player (0-len(playerIDs))][position (0-2)]
	# Transpose so that players are indexed on outside, easier to interperet for debugging

	vpipM =    transpose(calcPercent(vpip, handsPlayed, 3)) # Calculates percentages for each preflop statistic
	pfrM =     transpose(calcPercent(pfr,  handsPlayed, 3))
	tbpM =     transpose(calcPercent(tbp,  handsPlayed, 4))
	wtsdM =    transpose(calcPercent(wtsd, handsPlayed, 3))
	wasdM =    transpose(calcPercent(wasd, handsPlayed, 3)) # Calculates percentage relative to hands played
	wasdRelM = transpose(calcPercent(wasd, wtsd,        3)) # Calculates percentage relative to times WTSD

	cbpM =     transpose(calcPercent(cbp[0:2], cbp[2:4],2)) # "                     of c-bet relative to opportunities

	cbpCountM = transpose(cbp)

	afM =  transpose(calcAF (af,  actionCount, 2))
	afqM = transpose(calcAFQ(afq, actionCount, 3))

	bestHandsM = transpose(bestHands)

	# --------------------------------------------------------------------------------------------

	path_ledger = "Ledgers/ledger_{}.xls".format(date)
	ledgerM = calcLedger(path_ledger, playerIDs)

	# ---------------------------------------------------------------------------------------------
	# Now, the output functions:
	# 1. List of players
	# 2. Date of session
	# 3. Type of poker analyzed (pokerType)
	# 4. Statistics & bankroll

	# print('The following people played this session:')
	playerNames = []
	for ID in playerIDs: playerNames.append(playerDict[ID])

	whoPlayedWhen(playerNames, playerIDs, dateFormat)

	assert len(playerNames) == len(playerIDs), 'One or more player IDs are not in dictionary!'

	if   holdEm == True  and PLO == False: pokerType = 'No Limit Texas Hold\'em\n'
	elif holdEm == False and PLO == True : pokerType = 'Pot Limit Omaha\n'
	elif holdEm == True  and PLO == True : pokerType = 'No Limit Texas Hold\'em & PLO\n'
	else: 								   pokerType = "N/A"

	playerIndices = assignPlayerIndices(playerIDs, playerNames)

	if len(playerNames) > 0:
		# Call this to see all stats for all players in session ------------------------------------

		if includeCMD[handTypeDesired] == 1:
			printAllStatsForAllPlayers(vpipM, pfrM, tbpM, cbpM, cbpCountM, afM, afqM, wtsdM, 
									   wasdM, mwas, mwbs, ledgerM, playerDict, playerIDs, 
									   handsPlayed, bestHandsM, wasdRelM)

		# Now, write current session stats for all players to Excel --------------------------------

		writeCurrSessionToExcel(vpipM, pfrM, tbpM, cbpCountM, afM, afqM, wtsdM, wasdM, mwas,
								mwbs, ledgerM, playerIDs, playerDict, handsPlayed, bestHandsM, 
								dateFormat, handTypeDesired, wasdRelM)

		# Now, write dataframe containing stack/net data to Excel, then create charts with openpyxl

		writeStacksOverTimetoExcel(sessionStacks, playerNames, stackChangeInfo, playerIDs, 
								   handTypeDesired, dateFormat)

		#### TRANS-SESSION STATS -------------------------------------------------------------------------------

		# Keep track of stats across multiple sessions, much like bankrolls ------------------------

		writeStatsOverTimetoExcel(vpipM, pfrM, tbpM, cbpM, afM, afqM, wtsdM, wasdRelM, mwas, mwbs, 
								  playerIndices, dateFormat, handTypeDesired)

		# Update the all-time bankrolls for players if not already entered -------------------------

		writeBankrollsToExcel(ledgerM, dateFormat, playerIndices)

		# Update the all-time stats for players if not already entered -----------------------------

		writeAvgStatstoExcel(vpipM, pfrM, tbpM, cbpCountM, afM, afqM, wtsdM, wasdM, wasdRelM, 
							 mwas, mwbs, ledgerM, playerIndices, handsPlayed, date, handTypeDesired)

	else: 
		# print('No {} hands were played on {}.\n'.format(handTypeDesired, dateFormat))
		wipeCurrSessionSheets(handTypeDesired)

	# ----------------------------------------------------------------------------------------------

	output = (dateFormat, playerNames, pokerType) # output to display on the tkinter GUI

	return output
