import copy
from search import *
from subtract import *

def calcNetStacks(sessionStacks, stackChangeInfo, playerIDs):

	stacks = copy.deepcopy(sessionStacks)

	prevNumPlayers = 0
	startingStacks = []
	net = []

	for i in range(len(stacks)): # loops through every hand
		numPlayers = len(stacks[i])

		if numPlayers > prevNumPlayers: # 1 or more people joined the session
			playersAdded = numPlayers - prevNumPlayers

			for k in range(playersAdded):
				stackIdx = prevNumPlayers+k
				startingStacks.append(stacks[i][stackIdx]) # append the player's starting stack from the end of stacks

		# Now, change ONLY startingStacks in this loop
		for (idx, tuple) in enumerate(stackChangeInfo):
			if tuple[2] == i+1: # Player is adding on this hand
				addOnID = tuple[0]
				addOnAmount = tuple[1]

				playerIdx = search(playerIDs, addOnID)

				startingStacks[playerIdx] += (addOnAmount/100)

		currNet = subtract(sessionStacks[i], startingStacks)
		net.append(currNet)

		prevNumPlayers = numPlayers

	return net


	
