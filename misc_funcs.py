import numpy as np
import pandas as pd

def search(list, platform): # search for platform in list
# returns index or -1
    for (i, item) in enumerate(list):
        if item == platform:
            return i
    return -1


def appendMultiple(list, additions):
	# appends multiple indices on end of 2D list
	for i in range(len(list)):
		list[i] += [0]*additions


def appendMultiple3D(list, additions):
	# appends multiple indices on end of 3D list
	for i in range(len(list)):
		for j in range(len(list[i])):
			list[i][j] += [0]*additions


def resetList(list):
	for i in range(len(list)): list[i] = 0


def transpose(list):
	numpy_array = np.array(list)
	transpose = numpy_array.T
	Tlist = transpose.tolist()

	return Tlist


def isMatch(str1, str2):
	# Determines whether two strings are a close match or not
	if str1.lower() == str2.lower():
		return True

	# More matching below using regex
	pass

	return False


def replaceSuits(str):
	# Replaces output suit strings with readable suits

	# str = str.replace('â™¥', '♥️')
	# str = str.replace('â™¦', '♦')
	# str = str.replace('â™£', '♣')
	# str = str.replace('â™ ', '♠')

	str = str.replace('â™¥', 'h')
	str = str.replace('â™¦', 'd')
	str = str.replace('â™£', 'c')
	str = str.replace('â™ ', 's')

	return str


def howManyTens(str):
	tens = 0

	while str.find('10') != -1: # tens are still lurking
		tens += 1
		str = str[str.find('10') + 2:]

	return tens


def whichHandType(str, handType):
	# Returns which hand type is being played now: Hold em or PLO

	if   str.find('No Limit Texas Hold\'em') != -1: handType = 'NL'
	elif str.find('Pot Limit Omaha Hi'     ) != -1: handType = 'PLO'
	assert handType != None, 'Something is wrong, there should be a hand type'

	return handType


def createPlayerDict():
	# Creates dictionary for poker stats to use to identify players by their nicknames
	# Uses a text file in the folder <playerDictionary.txt>

	playerDict = {}
	f = open('playerDictionary.txt', 'r')

	for i, line in enumerate(f):

		line = line.replace('\n', '')
		if i % 2 == 0:      # even lines are keys
			key = line
		else:               # odd lines are names
			name = line
			playerDict[key] = name

	f.close()

	return playerDict


def addToPlayerDict(id, name):
	# Adds new player and their nickname this session to the dictionary
	# in the correct format

	f = open('playerDictionary.txt', 'a')

	f.write('\n{}'.format(id))
	f.write('\n{}'.format(name))

	f.close()


def capturePlayerStacks(str, stacks, playerIDs, currPlayerIDs):

	prevAtIndex = 0
	
	for i in range(len(currPlayerIDs[0])):

		atIndex = str.find('@', prevAtIndex+1) # find next @ symbol before ID
		tempID = str[atIndex+2:atIndex+2+10] # 10 character player ID

		playerIndex = search(playerIDs, tempID)

		prevAtIndex = atIndex

		# Find stack amount
		openIndex = str.find('(', prevAtIndex+1) # find next ( symbol, indicating a stack declaration
		closeIndex = str.find(')', prevAtIndex+1)

		stack = int(str[openIndex+1:closeIndex]) # stack

		stacks[playerIndex] = stack/100 # fill correct index with stack

	return stacks


def numPlayersIn(list):
	# Checks list to see if any other indices besides the one given as an argument
	# are not zero. Used to scan the list for other players that are still in at
	# showdown.
	playersIn = 0
	for item in list:
		if item == 0: # player is still in
			playersIn += 1

	return playersIn


def assignDealer(str):
	# save dealer ID in temp variable
	atIndex = str.find('@')
	dealerID = str[atIndex+2:atIndex+2+10] # 10 character player ID
	return dealerID


def assignPositions(str, dealerID, playerIDs, currPlayerIDs, handsPlayed, hasFolded):
	# Assigns new players an index, seat, and position
	# Assigns old players a seat and position

	# Start by assigning new players to an index
	playersAdded = 0 # so we know how to append the stats lists

	prevAtIndex = 0

	while str.find('@', prevAtIndex+1) != -1: # while another player ID can still be found,
		# add new players to list

		atIndex = str.find('@', prevAtIndex+1) # find next @ symbol before ID
		tempID = str[atIndex+2:atIndex+2+10] # 10 character player ID

		currPlayerIDs[0].append(tempID) # add player ID to list for this hand
		hasFolded.append(0)
		
		if search(playerIDs, tempID) == -1: # new player has been found
			playerIDs.append(tempID) # add new player ID to main list
			playersAdded += 1

		prevAtIndex = atIndex # hold past index to make sure to find new @ symbol

	appendMultiple(handsPlayed, playersAdded)

	# ---------------------------------------------------------------------------------------

	# Next, assign each player to a seat.
	prevSeatIndex = 0

	while str.find('#', prevSeatIndex+1) != -1:
		seatIndex = str.find('#',prevSeatIndex+1) + 1 # find number that shows seat
		seat = int(str[seatIndex:seatIndex+2]) # assign seat index

		currPlayerIDs[1].append(seat)

		prevSeatIndex = seatIndex # hold past index to make sure to find new "#" symbol

	# ---------------------------------------------------------------------------------------

	numPlayers = len(currPlayerIDs[0])

	# ---------------------------------------------------------------------------------------

	# Assign positions for the hand
	dealerIndex = search(currPlayerIDs[0], dealerID)

	temp = [0] * numPlayers
	currPlayerIDs[2].extend(temp) # preallocate space for positions

	for i in range(numPlayers): # loop through seat numbers
		currPlayerIDs[2][(dealerIndex+i) % numPlayers] = i # fill positions, wrap around list

	#----------------------------------------------------------------------------------------

	# Determine whether position is early or late
	for i in range(numPlayers):
		playerIdx = search(playerIDs, currPlayerIDs[0][i])

		if currPlayerIDs[2][i]/numPlayers < 0.5: # late position for the hand
			position = 'late'
			handsPlayed[1][playerIdx] += 1 # add hand played in late pos

		else: # early position for the hand
			position = 'early'
			handsPlayed[0][playerIdx] += 1 # add hand in early pos

		currPlayerIDs[2][i] = position

	return playersAdded


def countAction(actionID, action, actionCount, currPlayerIDs, playerIDs):
	actions = ['bets', 'raises', 'calls', 'folds']
	
	# 1. Find position of player
	actionPlayerIndex = search(currPlayerIDs[0], actionID)
	# print(actionPlayerIndex)
	position = currPlayerIDs[2][actionPlayerIndex]

	# 2. Find index of player in playerIDs
	# Overwrite previous index, that index was only used for position, no longer needed
	actionPlayerIndex = search(playerIDs,actionID)

	# 2. Find index of action based on list defined above
	actionIndex = search(actions, action)

	#3. Add the action to the action count
	if position == 'early':
		actionCount[actionIndex][0][actionPlayerIndex] += 1

	else: # position == 'late'
		actionCount[actionIndex][1][actionPlayerIndex] += 1


def assignPlayerIndices(playerIDs, playerNames):
	# Arguments: playerIDs:   current 10-digit IDs of players this session
	#            playerNames: nicknames used by the players this session.
	# Returns:   tuple of player indices for the session.

	""" Trans-session stats all commonly require that the 4 tracked players' trans-session indices
		(Fish = 0, Raymond = 1, Scott = 2, Cedric = 3) are mapped to the current session indices
		within playerIDs. Remember, playerIDs is appended according to the order in which players
		join the session.

		This function maps those indices, matching the ID in playerIDs to one of the saved IDs for the
		tracked player.

		Tracked players also may use new IDs unexpectedly, not matching any saved ID. Instead of assuming 
		the tracked player didn't play, it tries to match the player's nickname used during the session 
		(contained in playerNames) to one of the saved nicknames. These nicknames have commonly been
		used in the past.

		If it matches within a certain margin of error, it will add the player's new ID to the saved IDs
		and add the player's stats. It will also send an informational message to the GUI regarding the 
		changes.

		If neither method works, the function will make the index -1, and assume the player did not play.
	"""

	trackedIDs = []
	trackedNames = []

	# filenames = os.listdir('Tracked Players') # out of order, must code manually
	filenames = ['Fish_IDs.txt', 'Fish_names.txt', 'Raymond_IDs.txt', 'Raymond_names.txt', 
	             'Scott_IDs.txt', 'Scott_names.txt', 'Cedric_IDs.txt', 'Cedric_names.txt']

	# 1. Get IDs & names from files -------------------------------------------

	for i, filename in enumerate(filenames): # Go through all files with names and IDs
	    temp = list()

	    file = open(r'Tracked Players\{}'.format(filename), 'r')
	    for line in file:
	        line = line.replace('\n', '')
	        temp.append(line)

	    if i % 2 == 0: # file is even, is an ID file
	        trackedIDs.append(temp)
	    else:          # file is odd, it is a name file
	        trackedNames.append(temp)

	    file.close()

	# 2. Map indices ----------------------------------------------------------

	numPlayers = len(playerIDs)
	mappedIndices = [-1] * 4 
	newIDs = [''] * 4 # Any new IDs that are found must be stored

	for pI, tuple in enumerate(trackedIDs):
	    for trackedID in tuple:
	        for i, ID in enumerate(playerIDs):
	            if trackedID == ID:
	                # Add index to mappedIndices
	                mappedIndices[pI] = i

	# print(mappedIndices)

	# Iterate through indices. If -1, start matching
	for i, index in enumerate(mappedIndices):
	    if index == -1: # No match found above
	        # First, get list of tracked names
	        for trackedName in trackedNames[i]:
	            for j, name in enumerate(playerNames):
	                if isMatch(name, trackedName):
	                    # Found it!
	                    mappedIndices[i] = j
	                    newIDs[i] = playerIDs[j]

	# print(mappedIndices)
	# print(newIDs)

	# 3. Write new IDs to correct file -----------------------------------------
	mynames = ('Fish', 'Raymond', 'Scott', 'Cedric')

	for i, newID in enumerate(newIDs):
	    if newID != '':
	        file = open(r'Tracked Players\{}_IDs.txt'.format(mynames[i]), 'a')
	        file.write('{}\n'.format(newID))
	        file.close()

	return mappedIndices


def whoPlayedWhen(names, IDs, date):
	# Stores player nicknames and IDs into a text file
	# This will help reference who played what session as there are more sessions
	path = r'Outputs\whoPlayedWhen.txt'

	f = open(path, 'r')

	prevDates = []

	for (i, line) in enumerate(f):
		if 'Date: ' in line:
			line = line.replace('\n', '')
			prevDates.append(line[6:]) # Text past 'Date: '

	f.close()

	# --------------------------------------------------------------------------

	f = open(path, 'a')

	if date not in prevDates:
		print('Storing names and IDs for this session...')

		line1 = ('Date: ', date, '\n')
		
		f.writelines(line1)

		for (i, ID) in enumerate(IDs):
			f.write(ID)
			f.write('     ')
			f.write(names[i])
			f.write('\n')

		f.write('\n')

	f.close()


def average(statAvg, statThisSession, totalHandsPlayed, handsPlayedThisSession):
	
	newTotal = totalHandsPlayed + handsPlayedThisSession # total hands played over previous sessions and
														 # this session combined

	weightedAverage = (statThisSession*(handsPlayedThisSession/newTotal)) + (statAvg*(totalHandsPlayed/newTotal))

	return weightedAverage