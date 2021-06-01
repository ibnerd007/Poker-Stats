import copy

def calcNetStacks(sessionStacks):

	stacks = copy.deepcopy(sessionStacks)

	prevNumPlayers = 0
	startingStacks = []
	net = [[]]

	for i in range(len(stacks)):
		numPlayers = len(stacks[i])

		if numPlayers > prevNumPlayers: # 1 or more people joined the session
			playersAdded = numPlayers - prevNumPlayers

			for k in range(playersAdded):
				stackIdx = prevNumPlayers+k
				startingStacks.append(stacks[i][stackIdx]) # append the player's starting stack from the end of stacks

		for j in range(numPlayers):
			pass


		prevNumPlayers = numPlayers

	# print(startingStacks)

	
