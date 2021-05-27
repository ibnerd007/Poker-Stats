import math
import time

def calcAvgSessionStacks(stacks, n):
	# n = number of hands to average
	
	avgStacks = []
	prevNumPlayers = 0
	iEffectives = []
	
	for i in range(len(stacks)): # loop through entire session starting stacks
		avgStacks.append([])
		numPlayers = len(stacks[i]) # get the number of players in the session
		
		if numPlayers > prevNumPlayers: # 1 or more people joined the session
			playersAdded = numPlayers - prevNumPlayers
			for k in range(playersAdded):
				iEffectives.append(0) # Keep track of separate MAVG counters for each player

		for j in range(numPlayers): # Loop through players that have joined so far
		
			avgStacks[i].append(0)

			iEff = iEffectives[j] # set the current iEffective

			if iEff < n: # 10 hands haven't been played yet
				for counter in range(iEff+1):
					avgStacks[i][j] += stacks[i-counter][j]
				avgStacks[i][j] /= (iEff+1)

			else: # iEff >= n
				for counter in range(n):
					avgStacks[i][j] += stacks[i-counter-1][j]
				avgStacks[i][j] /= n

		iEffectives = [iEff+1 for iEff in iEffectives] # increment effective i counters

		prevNumPlayers = numPlayers # set players so that in next iteration new players will be found

	for i in range(len(stacks)):
		for j in range(len(stacks[0])):
			avgStacks[i][j] = round(avgStacks[i][j], 2) # After division, round all values to 2 decimal places

	return avgStacks

