from search import *

def countAction(actionID, action, actionCount, currPlayerIDs, playerIDs):
	actions = ['bets', 'raises', 'calls', 'folds']
	
	# 1. Find position of player
	actionPlayerIndex = search(currPlayerIDs[0], actionID)
	# print(actionPlayerIndex)
	position = currPlayerIDs[2][actionPlayerIndex]

	# 2. Find index of player in playerIDs
	# Overwrite previous index, that index was only used for position, no longer needed
	actionPlayerIndex = search(playerIDs,actionID)

	# 2. Find index of action based on list defined above
	actionIndex = search(actions, action)

	#3. Add the action to the action count
	if position == 'early':
		actionCount[actionIndex][0][actionPlayerIndex] += 1

	else: # position == 'late'
		actionCount[actionIndex][1][actionPlayerIndex] += 1