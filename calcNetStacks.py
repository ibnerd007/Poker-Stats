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
				startingStacks.append(stacks[i][stackIdx]) # append the player's starting stack to the end of stacks

		# Now, change ONLY startingStacks in this loop for add ons
		for (idx, tuple) in enumerate(stackChangeInfo):
			addOnHand = tuple[2]

			if addOnHand-1 == i: # Player is adding on next hand
				addOnID = tuple[0]
				amount =  tuple[1]
				isReset = tuple[3]

				playerIdx = search(playerIDs, addOnID)
				
				if isReset:	amount -= stacks[i-1][playerIdx]*100 # subtract current stack from reset amount

				startingStacks[playerIdx] += amount/100

		currNet = subtract(stacks[i], startingStacks)
		net.append(currNet)

		prevNumPlayers = numPlayers

	assert len(stacks) == len(net)

	return net


	
