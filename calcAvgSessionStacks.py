import math

def calcAvgSessionStacks(stacks, n):
	# n = number of hands to average

	avgStacks = []
	prevNumPlayers = 0
	iEffectives = []
	
	for i in range(len(stacks)): # loop through entire session starting stacks
		avgStacks.append([]) 
		numPlayers = len(stacks[0]) # get the number of players in the session
		
		if numPlayers > prevNumPlayers: # 1 or more people joined the session
			playersAdded = numPlayers - prevNumPlayers
			for k in range(playersAdded):
				iEffectives.append(i) # Keep track of separate MAVG counters for each player

		for j in range(numPlayers): # Loop through players that have joined so far

			avgStacks[i].append(0)

			iEff = iEffectives[j] # set the current iEffective

			if i < n: # 10 hands haven't been played yet
				for counter in range(i+1):
					avgStacks[i][j] += stacks[i-counter][j]
				avgStacks[i][j] /= (i+1)

			else: # iEff >= n
				for counter in range(n):
					avgStacks[i][j] += stacks[i-counter-1][j]
				avgStacks[i][j] /= n

		iEffectives = [iEff+1 for iEff in iEffectives] # increment effective i counters

		prevNumPlayers = numPlayers

	for i in range(len(stacks)):
		for j in range(len(stacks[0])):
			avgStacks[i][j] = round(avgStacks[i][j], 2)

	print('Length of avgStacks = ', len(avgStacks))

	return avgStacks

