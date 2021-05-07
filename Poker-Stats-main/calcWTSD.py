from search import *

def calcWTSD(wtsd, hasFolded, playerIDs, currPlayerIDs):
	for i in range(len(hasFolded)): # hasFolded
		if hasFolded[i] != 1: # player did not fold in the hand (went to showdown)

			sdID = currPlayerIDs[0][i] # Find ID of the champion who went to showdown
			position = currPlayerIDs[2][i]
			wtsdIndex = search(playerIDs,sdID)
			

			if position == 'early':
				wtsd[0][wtsdIndex] += 1
			else:
				wtsd[1][wtsdIndex] += 1