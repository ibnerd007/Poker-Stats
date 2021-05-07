from search import *

def calcWASD(wasd, sdID, playerIDs, currPlayerIDs):

	sdIDIndex = search(currPlayerIDs[0], sdID) # to get position only
	position = currPlayerIDs[2][sdIDIndex]

	wasdIndex = search(playerIDs,sdID)
	# print(wasdIndex)


	if position == 'early':
		wasd[0][wasdIndex] += 1
	else:
		wasd[1][wasdIndex] += 1