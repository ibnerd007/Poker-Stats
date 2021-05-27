import copy
import time

def calcNetStacks(sessionStacks):

	stacks = copy.deepcopy(sessionStacks)
	print(stacks)

	prevNumPlayers = 0
	startingStacks = []
	net = [[]]

	for i in range(len(stacks)):
		print('i = ', i)
		numPlayers = len(stacks[i])

		if numPlayers > prevNumPlayers: # 1 or more people joined the session
			playersAdded = numPlayers - prevNumPlayers

			for k in range(playersAdded):
				stackIdx = prevNumPlayers+k
				print('stackIdx: ', stackIdx)
				time.sleep(0.01)
				startingStacks.append(stacks[i][stackIdx]) # append the player's starting stack from the end of stacks

		for j in range(numPlayers):
			pass


		prevNumPlayers = numPlayers

	print(startingStacks)

	
