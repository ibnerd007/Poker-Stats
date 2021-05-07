import xlrd
import math

from startingHandNumber import *
from assignPositions import *
from appendMultiple import *
from appendMultiple3D import *
from getID import *

from calcVPIP import *
from calcPFR import *
from calcTBP import *
from countAction import *
from calcAF import *
from calcAFQ import *
from calcWTSD import *
from calcWASD import *


from resetList import *
from calcPercentAndTranspose import *
from transpose import *

# Find path_log to Excel spreadsheet with log

path_log = "Logs/log_5 4.xls"

book = xlrd.open_workbook(path_log)
sheet = book.sheet_by_index(0)
rows = sheet.nrows

# The following lists keep track of specific stats; indexed by player ----------------------------------------

# Ex: vpip/pfr/tbp = [[fish_early, raymond_early, ...], [fish_late, raymond_late, ...], [fish_alreadyCounted, ...]]
# Ex: actionCount = [[[betCount_early_fish, betCount_early_ray,...], [betCount_late_fish, betCount_late_ray]], [callCount_early_fish, callCount_early_ray, ...], ...]
# Ex: af = [[af_early_fish, af_early_ray, ...], [af_late_fish, af_late_ray, ...]]
# Ex: wtsd = [[wtsd_early_fish, wtsd_early_ray, ...], [wtsd_late_fish, wtsd_late_ray, ...]]

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

# mwbs = [] # money won before showdown ($)
# bbWonPerFiftyHands = [] # Big Blinds won per 50 hands

# -----------------------------------------------------------------------------------------------------------

playerIDs = []
handsPlayed = [] # both indexed for each player. Order does not change throughout session.


# Static variables
bb = 20 # cents

# Variables changing within while loop
totalPlayed = 0 # total # of hands played
beforeFlop = False
hasRaised = False # there is a raise on the table

# Counter for entire log, choose where to start --------------------------------------------------------------
i = 0

while (i < rows):
	# Step 1: Parse line beginning with "starting hand #", then 'Player stacks:', then certain actions
	
	str = sheet.cell_value(i,0) # get the string for the entire line

	# Preflop -------------------------------------------------------------

	if (str.find('starting hand #') != -1): # row found, indicates starting new hand
		dealerID = startingHandNumber(str) # dealer ID is determined and returned from this function
		currPlayerIDs = [[], [], []] # ID, seat, position. This is reset every hand
		hasFolded = [] # Tracks who has folded in the hand
		hasCollected = [] # If a player collects a main pot and side pot, they only win at showdown once
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
		# print(currPlayerIDs)

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
	# These stats are NOT position-based
	if str.find('collected') != -1 & str.find('combination') != -1: # someone has won the pot at showdown
		wasdID = getID(str)

		calcWASD(wasd, wasdID, playerIDs, currPlayerIDs, hasCollected)
		hasCollected.append(wasdID) # player has won and can't win again if a side pot is also collected
		print(wasd)
		# print(wasd)

	if str.find('ending hand #') != -1: # hand has ended
		calcWTSD(wtsd, hasFolded, playerIDs, currPlayerIDs) # Any player that hasn't folded now, has gone to showdown

	i += 1
	print(i)
# ------------------------------------------------------------------------------------------

# Calculate stats by player in early, late, and total position

vpipM = calcPercentAndTranspose(handsPlayed, vpip, 3)
pfrM = calcPercentAndTranspose(handsPlayed, pfr, 3)
tbpM = calcPercentAndTranspose(handsPlayed, tbp, 4) # Calculates percentages for each preflop statistic
wtsdM = calcPercentAndTranspose(handsPlayed, wtsd, 3)
wasdM = calcPercentAndTranspose(handsPlayed, wasd, 3)
# print(wtsdM)

af = calcAF(af, actionCount, 2)
afq = calcAFQ(afq, actionCount, 3)
afM = transpose(af)
afqM = transpose(afq)

# print(handsPlayed)
print(playerIDs, '\n')

# ------------------------------------------------------------------------------------------

# With all stats calculated, add them to a class to easily look up per player

staticIDs = ['L5G0fi1P1T','gpL6BdHM3Z','UOl9ieuNTH','DAovHf6aFe','-4Mt9GCcpf','J_J1Sm6uON',
			 'Tfv9gQlCKp','zQzHYg1f_X','EUC1-Ekcwo','FHfdGMNnXa','UPoeIpvEQ4']
#             fish,        raymond,     cedric,      cheyenne,    scott,       tristan,     
#             kynan,       xavier,      bill,        marshall,    regan


# k list allows the program to find the same players every session, regardless of order

k = [0] * len(staticIDs) # number of players
for i in range(len(k)):
	k[i] = search(playerIDs, staticIDs[i])

class Player:

	def __init__(self, name, vpip, pfr, tbp, af, afq, wtsd, wasd):
		self.name = name
		self.vpip = vpip # voluntarily put in pot (%)
		self.pfr = pfr # pre-flop raise (%)
		self.tbp = tbp # 3 bet percentage
		self.af = af # aggression factor
		self.afq = afq # aggression frequency (%)
		self.wtsd = wtsd # went to showdown (%)
		self.wasd = wasd # went to showdown (%)
		# self.bbWon = bbWon # bb won per fifty hands

	def stats(self, position=''):

		args = ['early', 'late', '']

		i = search(args, position)
		assert args[i] != -1, 'Enter a valid argument'

		if position == '': # stat averages have been requested
			print('stat averages for', self.name)
		else:
			print(args[i], 'stats for', self.name)
		print("VPIP             :", self.vpip[i])
		print("Pre-flop raise   :", self.pfr[i])
		print("Three-bet        :", self.tbp[i], '\n')
		print("Aggression factor:", self.af[i])
		print("Aggression freq  :", self.afq[i])
		print("\nWent to showdown  :", self.wtsd[i])
		print("Won at showdown   :", self.wasd[i])

fish = Player("Fish", vpipM[k[0]], pfrM[k[0]], tbpM[k[0]], afM[k[0]], afqM[k[0]], wtsdM[k[0]], wasdM[k[0]])

raymond = Player("Raymond", vpipM[k[1]], pfrM[k[1]], tbpM[k[1]], afM[k[1]], afqM[k[1]], wtsdM[k[1]], wasdM[k[1]])

cedric = Player("Cedric", vpipM[k[2]], pfrM[k[2]], tbpM[k[2]], afM[k[2]], afqM[k[2]], wtsdM[k[2]], wasdM[k[2]])

cheyenne = Player("Cheyenne", vpipM[k[3]], pfrM[k[3]], tbpM[k[3]], afM[k[3]], afqM[k[3]], wtsdM[k[3]], wasdM[k[3]])

scott = Player("Scott", vpipM[k[4]], pfrM[k[4]], tbpM[k[4]], afM[k[4]], afqM[k[4]], wtsdM[k[4]], wasdM[k[4]])

tristan = Player("Tristan", vpipM[k[5]], pfrM[k[5]], tbpM[k[5]], afM[k[5]], afqM[k[5]], wtsdM[k[5]], wasdM[k[5]])

kynan = Player("Kynan", vpipM[k[6]], pfrM[k[6]], tbpM[k[6]], afM[k[6]], afqM[k[6]], wtsdM[k[6]], wasdM[k[6]])

xavier = Player("Xavier", vpipM[k[7]], pfrM[k[7]], tbpM[k[7]], afM[k[7]], afqM[k[7]], wtsdM[k[7]], wasdM[k[7]])

bill = Player("Bill", vpipM[k[8]], pfrM[k[8]], tbpM[k[8]], afM[k[8]], afqM[k[8]], wtsdM[k[8]], wasdM[k[8]])

marshall = Player("Marshall", vpipM[k[9]], pfrM[k[9]], tbpM[k[9]], afM[k[9]], afqM[k[9]], wtsdM[k[9]], wasdM[k[9]])

regan = Player("Regan", vpipM[k[10]], pfrM[k[10]], tbpM[k[10]], afM[k[10]], afqM[k[10]], wtsdM[k[10]], wasdM[k[10]])


# assert k[4] != -1, 'This player didn\'t play this session'
fish.stats()


print('Done!')
