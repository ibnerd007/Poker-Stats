from search import *

def getPlayerStacks(str, stacks, playerIDs, currPlayerIDs):

	prevAtIndex = 0
	
	for i in range(len(currPlayerIDs[0])):

		atIndex = str.find('@', prevAtIndex+1) # find next @ symbol before ID
		tempID = str[atIndex+2:atIndex+2+10] # 10 character player ID

		playerIndex = search(playerIDs, tempID)
		print(playerIDs)
		print('Player index:', playerIndex)

		prevAtIndex = atIndex

		# Find stack amount
		openIndex = str.find('(', prevAtIndex+1) # find next ( symbol, indicating a stack declaration
		closeIndex = str.find(')', prevAtIndex+1)

		stack = int(str[openIndex+1:closeIndex]) # stack'

		stacks[playerIndex] = stack/100 # fill correct index with stack

