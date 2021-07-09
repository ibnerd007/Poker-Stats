from misc_funcs import search, appendMultiple, howManyTens, replaceSuits


def calcVPIP(vpipID, vpip, playerIDs, currPlayerIDs):
	# Every hand, looks for players that call or raise preflop

	i = search(currPlayerIDs, vpipID) # for finding position ONLY
	j = search(playerIDs, vpipID) # for adding whole stat

	position = currPlayerIDs[2][i] # 'early' or 'late'

	if position == 'early' and vpip[2][j] == 0:
		vpip[0][j] += 1
	elif position == 'late' and vpip[2][j] == 0: # late position, no vpip added previously
		vpip[1][j] += 1

	vpip[2][j] = 1 # already added, don't add call or raise again until next hand


def calcPFR(pfrID, pfr, playerIDs, currPlayerIDs):
	# Every hand, looks for players that call or raise preflop

	i = search(currPlayerIDs, pfrID) # for finding position ONLY
	j = search(playerIDs, pfrID) # for adding whole stat

	position = currPlayerIDs[2][i] # 'early' or 'late'

	if position == 'early' and pfr[2][j] == 0:
		pfr[0][j] += 1
	elif pfr[2][j] == 0: # late position, no pfr added previously
		pfr[1][j] += 1

	pfr[2][j] = 1 # already added, don't add call or raise again until next hand


def calcTBP(tbID, tbp, playerIDs, currPlayerIDs):

	i = search(currPlayerIDs, tbID) # for finding position ONLY
	j = search(playerIDs, tbID) # for adding whole stat

	position = currPlayerIDs[2][i] # 'early' or 'late'

	if position == 'early' and tbp[2][j] == 0:
		tbp[0][j] += 1

	elif tbp[2][j] == 0: # late position, no tbp added previously
		tbp[1][j] += 1

	tbp[2][j] = 1 # already added, don't add 3 bet again for that person until next hand


def calcCBP(str, cbp, aggressorID, playerIDs, currPlayerIDs):
	# designates opportunities for c-bets and c-bets of all players positionally
	# This function analyzes the aggressor's action post-flop but before turn for a c-bet

	aggressorIdx = search(playerIDs, aggressorID)
	assert aggressorIdx != -1, 'Aggressor not found in currPlayerIDs'
	aggressorPosition = currPlayerIDs[2][search(currPlayerIDs[0], aggressorID)]

	if str.find('bets') != -1: # aggressor c-bets from flop
	
		if aggressorPosition == 'early':
			cbp[2][aggressorIdx] += 1 # add 1 opportunity in early position
			cbp[0][aggressorIdx] += 1 # add 1 c-bet "
		else:
			cbp[3][aggressorIdx] += 1 # add 1 opportunity in late position
			cbp[1][aggressorIdx] += 1 # add 1 c-bet "

	elif str.find('checks') != -1: # agggressor has had the opportunity to c-bet but did not
		
		if aggressorPosition == 'early': cbp[2][aggressorIdx] += 1 # add 1 opportunity in early position
		else:                            cbp[3][aggressorIdx] += 1 # add 1 opportunity in late position

	else: # aggressor calls, raises, or folds
		pass # no opportunity to c-bet, player in front donked. *Assumes aggressor doesn't fold a free check*


def calcAF(af, count, decimals):
	# count[type][position][player]
	# af[position][player]

	# 1. Calculate aggression factor (af) for each player in early and late position
	# AF = (# bets + # raises)/(# calls)
	# actions = ['bets', 'raises', 'calls', 'folds']

	positions = len(count[0])
	numPlayers = len(count[0][0])

	for i in range(numPlayers):
		# Calculate aggression factor first based on position ------------------------------------
		for j in range(positions):

			aggressives = count[0][j][i] + count[1][j][i]
			calls = count[2][j][i]

			try:    tempAf = aggressives/calls
			except: tempAf = -1

			af[j][i] = round(tempAf, decimals)

		# Calculate average aggression factor across all positions -------------------------------
		allAggressives = count[0][0][i] + count[1][0][i] + count[0][1][i] + count[1][1][i]
		#               (early position                )  (late position                  )
		allCalls = count[2][0][i] + count[2][1][i]
		#         (early         ) (late          )

		try:    avgTempAf = allAggressives/allCalls
		except: avgTempAf = -1

		af[2][i] = round(avgTempAf, decimals)

	return af


def calcAFQ(afq, count, decimals):

	# count[type][position][player]
	# afq[position][player]

	# AFQ = (bets + raises)/(bets + raises + calls + folds)
	# actions = ['bets', 'raises', 'calls', 'folds']

	numPlayers = len(count[0][0])
	positions = len(count[0])

	for i in range(numPlayers): # player
		for j in range(positions): # position

			# Calculate aggression factor first based on position --------------------------------
			totalCount = count[0][j][i] + count[1][j][i] + count[2][j][i] + count[3][j][i]
			aggressives = count[0][j][i] + count[1][j][i]

			try:    tempAFQ = aggressives/totalCount
			except: tempAFQ = -1

			afq[j][i] = round(tempAFQ, decimals)

		# Calculate average aggression frequency across both positions -------------------------------
		allAggressives = count[0][0][i] + count[1][0][i] + count[0][1][i] + count[1][1][i]

		allTotalCount  = count[0][0][i] + count[1][0][i] + count[2][0][i] + count[3][0][i] + \
						 count[0][1][i] + count[1][1][i] + count[2][1][i] + count[3][1][i]

		avgTempAfq = allAggressives/allTotalCount

		afq[2][i] = round(avgTempAfq, decimals)

	return afq


def calcWTSD(wtsd, hasFolded, playerIDs, currPlayerIDs):
	for i in range(len(hasFolded)): # loop through who has folded
		if hasFolded[i] != 1: # went to showdown

			sdID = currPlayerIDs[0][i] # Find ID of the champion who went to showdown
			position = currPlayerIDs[2][i]
			wtsdIndex = search(playerIDs,sdID)

			assert position == 'early' or position == 'late', 'Invalid position'

			if position == 'early':
				wtsd[0][wtsdIndex] += 1
			if position == 'late':
				wtsd[1][wtsdIndex] += 1


def calcWASD(wasd, sdID, playerIDs, currPlayerIDs, hasCollected):

	sdIDIndex = search(currPlayerIDs[0], sdID) # to get position only
	position = currPlayerIDs[2][sdIDIndex]

	wasdIndex = search(playerIDs,sdID)

	assert position == 'early' or position == 'late', 'Invalid position'

	if search(hasCollected,sdID) == -1: # player has not yet collected in a showdown
		if position == 'early':
			wasd[0][wasdIndex] += 1
		if position == 'late':
			wasd[1][wasdIndex] += 1


def calcMWAS(mwas, pot, winnerID, playerIDs):
	i = search(playerIDs, winnerID)
	mwas[i] += pot # add money won at showdown, in dollars & cents


def calcMWBS(mwbs, pot, winnerID, playerIDs):
	i = search(playerIDs, winnerID)
	mwbs[i] += pot # add money won before showdown, in dollars & cents


from howManyTens import *
from replaceSuits import *

def calcBestHands(str, wI, bestHands):

	hands = ['Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 
			 'Four of a Kind', 'Straight Flush', 'Royal Flush']
	cardOrder = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

	tempStr = str[str.find('with'):] # Truncate string to only include parts about winning hand
	handStr = replaceSuits(tempStr) # Suits come into Excel incorrectly. This function corrects them

	currIndex = bestHands[1][wI] # bestHands[1][wI*] = rank (*winner index)
	newIndex = -1 # reset index

	for j in range(len(hands)):

		if handStr.find(hands[j]) != -1: # the winning hand has been identified
			# first, capture the high card, two characters if high card is a 10
			numTens = howManyTens(handStr[handStr.find('combination: ') + 13:handStr.find('combination: ') + 15])
			highCard = handStr[handStr.find('combination') + 13:
							   handStr.find('combination') + 14 + numTens]
	
			# Need to code some exceptions
			if hands[j] == 'Pair' and handStr.find('Two') != -1: # hand is actually two pair
				newIndex = 1 # two pair

			elif hands[j] == 'Flush':
				if handStr.find('Straight') != -1:
					newIndex = 7                     # straight flush
				elif handStr.find('Royal') != -1:
					newIndex = 8                     # royal flush
				else:
					newIndex = 4                     # just a flush

			else:
				newIndex = j # any other hand

		if (newIndex != -1 and newIndex > currIndex) or \
		   (newIndex == currIndex and search(cardOrder, highCard) > search(cardOrder, bestHands[3][wI])): # better hand OR better high card
				bestHands[0][wI] = hands[newIndex] # hand type, string
				bestHands[1][wI] = newIndex # new best hand ranking, for later comparison

				# Add hand combination for reporting later
				bestHands[2][wI] = handStr[handStr.find('combination: ') + 13: handStr.find(')')]
				bestHands[3][wI] = highCard # store high card for later comparison

				break # no need to continue checking if hand is better through the rest of hands


import xlrd
from appendMultiple import *
from transpose import *

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


def calcPercent(statCount, totalCount, decimals):
	# calculate actual statistic over course of hands played per player ------------------------
	
	numPlayers = len(statCount[0])

	earlyList = [0] * numPlayers
	lateList = [0] * numPlayers

	totalList =[] # for temporarily holding average stats across positions

	for i in range(numPlayers):
		x = totalCount[0][i]
		y = totalCount[1][i]

		try:    earlyList[i] = round(statCount[0][i]/x, decimals)
		except: earlyList[i] = 0

		try:    lateList[i] =  round(statCount[1][i]/y, decimals)
		except: lateList[i] =  0

		# Calculate stat averages now across both positions

		statTotal = statCount[0][i] + statCount[1][i]
		totalPlayed = totalCount[0][i] + totalCount[1][i]

		try:    total = round(statTotal/totalPlayed, decimals) # calculate average over all positions
		except: total = 0
			
		totalList.append(total) # add to overall list

	# Combine position and total lists ----------------------------------------------------------
	stat = [[0] * numPlayers] * 3 # Create a # players x 3 list (early, late, total)
	
	stat[0] = earlyList
	stat[1] = lateList
	stat[2] = totalList

	return stat
