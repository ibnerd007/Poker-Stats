from search import *

def calcWTSD(wtsd, hasFolded, playerIDs, currPlayerIDs):
	for i in range(len(hasFolded)): # loop through who has folded
		if hasFolded[i] != 1: # all players left went to showdown
			sdID = currPlayerIDs[0][i] # Find ID of the champion who went to showdown
			position = currPlayerIDs[2][i]
			wtsdIndex = search(playerIDs,sdID)

			# print('{} went to showdown.'.format(sdID))

			if position == 'early':
				wtsd[0][wtsdIndex] += 1
			if position == 'late':
				wtsd[1][wtsdIndex] += 1

			assert position == 'early' or position == 'late', 'Invalid position'