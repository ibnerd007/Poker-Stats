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

# Find path to Excel spreadsheet with log

date = '5 13'

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

# Static variables
bb = 20 # cents

# Variables changing within while loop
totalPlayed = 0 # total # of hands played
beforeFlop = False
hasRaised = False # there is a raise on the table

holdEm = False
PLO = False # possible hand types

# Counter for entire log, choose where to start --------------------------------------------------------------
i = 0
counter = 0

while (i < log_rows):
	# Step 1: Parse line beginning with "starting hand #", then 'Player stacks:', then certain actions
	
	str = log_sheet.cell_value(i,0) # get the string for the entire line

	# Preflop -------------------------------------------------------------

	if (str.find('starting hand #') != -1): # row found, indicates starting new hand
		dealerID = startingHandNumber(str) # dealer ID is determined and returned from this function
		currPlayerIDs = [[], [], []] # ID, seat, position. This is reset every hand
		hasFolded = [] # Tracks who has folded in the hand
		hasCollected = [] # If a player collects a main pot and side pot, they only win at showdown once

		if holdEm == False and str[str.find('(') + 1:str.find('(') + 23] == 'No Limit Texas Hold\'em':
			holdEm = True # At least one Hold Em hand was played
		elif PLO == False and str[str.find('(') + 1:str.find('(') + 19] == 'Pot Limit Omaha Hi':
			PLO = True # At least one PLO hand was played

		totalPlayed += 1

	if (str.find('Player stacks:') != -1): # row found, Players at table are now shown
		assert totalPlayed > 0, "You forgot to run the Excel macro; log order is reversed!"
		playersAdded = assignPositions(str, dealerID, playerIDs, currPlayerIDs, handsPlayed, hasFolded)

		# Add necessary elements to stat lists & counter 3D list to not over-index
		# list.append() won't work later on because elements will not be filed in order
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

		appendMultiple(bestHands, playersAdded)

		beforeFlop = True

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

	if str.find('ending hand #') != -1 and numPlayersIn(hasFolded) >= 2: # Shwodown hands only: hand has ended AND two or more players didn't fold
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
	assert idIndex != -1, 'Player ID not found in ledger'

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


# ------------------------------------------------------------------------------------------

# With all stats calculated, add them to a class to easily look up per player

staticIDs = ['L5G0fi1P1T','gpL6BdHM3Z','UOl9ieuNTH','DAovHf6aFe','-4Mt9GCcpf','J_J1Sm6uON',
			 'Tfv9gQlCKp','zQzHYg1f_X','EUC1-Ekcwo','FHfdGMNnXa','UPoeIpvEQ4', 'mZh56-rfJ5',
			 'LragqkH6mQ', 'pnFzv-_qqL', 'jvWHRQaeUN', 'wHCkaNaedp', 'FIgidiXEkn', 'IZfCYGmoLP',
			 'EZvsCiYcdt', 'RlQUK84X1Q']
#             fish,        raymond,     cedric,      cheyenne,    scott,       tristan,     
#             kynan,       xavier,      bill,        marshall,    regan,       jonathan,
#			  jacob,       cheyenne,    tristan,     jacob,       jacob,       jacob,
#             Dmkpro67,    colin

players = ['Fish', 'Raymond', 'Cedric', 'Cheyenne', 'Scott', 'Tristan',
		   'Kynan', 'Xavier', 'Bill', 'Marshall', 'Regan', 'Jonathan', 'Jacob',
		   'Cheyenne', 'Tristan', 'Jacob', 'Jacob', 'Jacob', 'Dmkpro67', 'Colin']


playerDict = {'L5G0fi1P1T': 'Fish', 'gpL6BdHM3Z': 'Raymond', 'UOl9ieuNTH': 'Cedric', 

			  'DAovHf6aFe': 'Cheyenne', '-4Mt9GCcpf': 'Scott', 'J_J1Sm6uON': 'Tristan',

		      'Tfv9gQlCKp': 'Kynan', 'zQzHYg1f_X': 'Xavier', 'EUC1-Ekcwo': 'Bill', 

		      'FHfdGMNnXa': 'Marshall', 'UPoeIpvEQ4': 'Regan', 'mZh56-rfJ5': 'Jonathan',

		      'LragqkH6mQ': 'Jacob', 'pnFzv-_qqL': 'Cheyenne', 'jvWHRQaeUN': 'Tristan', 

		      'wHCkaNaedp': 'Jacob', 'FIgidiXEkn': 'Jacob', 'IZfCYGmoLP': 'Jacob', 

		      'EZvsCiYcdt': 'Dmkpro67', 'RlQUK84X1Q': 'Colin'}


# k list allows the program to find the same players every session, regardless of order

# k = [0] * len(staticIDs) # number of players
# for i in range(len(k)):
# 	k[i] = search(playerIDs, staticIDs[i])

# class Player:

# 	def __init__(self, name, vpip, pfr, tbp, af, afq, wtsd, wasd, mwas, mwbs, ledger):
# 		self.name = name
# 		self.vpip = vpip # voluntarily put in pot (%)
# 		self.pfr = pfr # pre-flop raise (%)
# 		self.tbp = tbp # 3 bet percentage
# 		self.af = af # aggression factor
# 		self.afq = afq # aggression frequency (%)
# 		self.wtsd = wtsd # went to showdown (%)
# 		self.wasd = wasd # went to showdown (%)
# 		self.mwas = mwas # money won at showdown ($) *not position-based
# 		self.mwbs = mwbs # money won before showdown ($) *not position-based
# 		self.ledger = ledger # contains bankroll stats for each player
# 		# self.bbWon = bbWon # bb won per fifty hands

# 		# + or - for profit/loss sign convention
# 		if self.ledger[2] > 0: 
# 			self.PoL = '+' # profit
# 		else: 
# 			self.PoL = '-' # loss

# 	def posStats(self, position): # print stats to command line based on position

# 		args = ['early', 'late', 'avg'] # valid arguments for stats() method

# 		i = search(args, position)
# 		assert i != -1, 'Enter a valid position argument: early or late, or none for avg'

# 		# if isDecimal != '': # report in decimal form
# 		# 	reportDecimals(self, position, i)

# 		# else: # report in percentage form
# 		reportPercentages(self, position, i)

# 	def allStats(self): # print all stats to command line 
# 		printAllStatsForOnePlayer(self)


# fish = Player("Fish", vpipM[k[0]], pfrM[k[0]], tbpM[k[0]], afM[k[0]], afqM[k[0]], wtsdM[k[0]], wasdM[k[0]], mwas[k[0]], mwbs[k[0]], ledgerM[k[0]])

# raymond = Player("Raymond", vpipM[k[1]], pfrM[k[1]], tbpM[k[1]], afM[k[1]], afqM[k[1]], wtsdM[k[1]], wasdM[k[1]], mwas[k[1]], mwbs[k[1]], ledgerM[k[1]])

# cedric = Player("Cedric", vpipM[k[2]], pfrM[k[2]], tbpM[k[2]], afM[k[2]], afqM[k[2]], wtsdM[k[2]], wasdM[k[2]], mwas[k[2]], mwbs[k[2]], ledgerM[k[2]])

# cheyenne = Player("Cheyenne", vpipM[k[3]], pfrM[k[3]], tbpM[k[3]], afM[k[3]], afqM[k[3]], wtsdM[k[3]], wasdM[k[3]], mwas[k[3]], mwbs[k[3]], ledgerM[k[3]])

# scott = Player("Scott", vpipM[k[4]], pfrM[k[4]], tbpM[k[4]], afM[k[4]], afqM[k[4]], wtsdM[k[4]], wasdM[k[4]], mwas[k[4]], mwbs[k[4]], ledgerM[k[4]])

# tristan = Player("Tristan", vpipM[k[5]], pfrM[k[5]], tbpM[k[5]], afM[k[5]], afqM[k[5]], wtsdM[k[5]], wasdM[k[5]], mwas[k[5]], mwbs[k[5]], ledgerM[k[5]])

# kynan = Player("Kynan", vpipM[k[6]], pfrM[k[6]], tbpM[k[6]], afM[k[6]], afqM[k[6]], wtsdM[k[6]], wasdM[k[6]], mwas[k[6]], mwbs[k[6]], ledgerM[k[6]])

# xavier = Player("Xavier", vpipM[k[7]], pfrM[k[7]], tbpM[k[7]], afM[k[7]], afqM[k[7]], wtsdM[k[7]], wasdM[k[7]], mwas[k[7]], mwbs[k[7]], ledgerM[k[7]])

# bill = Player("Bill", vpipM[k[8]], pfrM[k[8]], tbpM[k[8]], afM[k[8]], afqM[k[8]], wtsdM[k[8]], wasdM[k[8]], mwas[k[8]], mwbs[k[8]], ledgerM[k[8]])

# marshall = Player("Marshall", vpipM[k[9]], pfrM[k[9]], tbpM[k[9]], afM[k[9]], afqM[k[9]], wtsdM[k[9]], wasdM[k[9]], mwas[k[9]], mwbs[k[9]], ledgerM[k[9]])

# regan = Player("Regan", vpipM[k[10]], pfrM[k[10]], tbpM[k[10]], afM[k[10]], afqM[k[10]], wtsdM[k[10]], wasdM[k[10]], mwas[k[10]], mwbs[k[10]], ledgerM[k[10]])

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

# Call this to see stats for one player --------------------------------------------
# assert k[0] != -1, 'This player didn\'t play this session'
# xavier.allStats()
# xavier.posStats('late')

# Call this to see all stats for all players in session ----------------------------

printAllStatsForAllPlayers(vpipM, pfrM, tbpM, afM, afqM, wtsdM, wasdM, mwas, mwbs, 
						   ledgerM, staticIDs, playerIDs, players, handsPlayed, bestHandsM)

# Now, write current session stats for all players to Excel ------------------------

# writeCurrSessionToExcel(vpipM, pfrM, tbpM, afM, afqM, wtsdM, wasdM, mwas, mwbs, 
# 			 ledgerM, staticIDs, playerIDs, playerDict, handsPlayed, bestHandsM)

# Update the all-time bankrolls for players if not already entered

# writeBankrollsToExcel(ledgerM, playerIDs, date)

print('Date: ', date, '\n')

