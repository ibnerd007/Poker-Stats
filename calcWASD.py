from search import *

def calcWASD(wasd, sdID, playerIDs, currPlayerIDs, hasCollected):

	sdIDIndex = search(currPlayerIDs[0], sdID) # to get position only
	position = currPlayerIDs[2][sdIDIndex]

	wasdIndex = search(playerIDs,sdID)

	if search(hasCollected,sdID) == -1: # player has not yet collected in a showdown
		if position == 'early':
			wasd[0][wasdIndex] += 1
		else:
			wasd[1][wasdIndex] += 1