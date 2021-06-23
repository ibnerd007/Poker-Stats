from search import *

def calcCBP(str, cbp, aggressorID, playerIDs, currPlayerIDs):
	# designates opportunities for c-bets and c-bets of all players positionally
	# This function analyzes the aggressor's action post-flop but before turn for a c-bet

	aggressorIdx = search(playerIDs, aggressorID)
	assert aggressorIdx != -1, 'Aggressor not found in currPlayerIDs'
	aggressorPosition = currPlayerIDs[2][search(currPlayerIDs[0], aggressorID)]

	if str.find('bets') != -1: # aggressor c-bets from flop
	
		if aggressorPosition == 'early':
			cbp[2][aggressorIdx] += 1 # add 1 opportunity in early position
			cbp[0][aggressorIdx] += 1 # add 1 c-bet "
		else:
			cbp[3][aggressorIdx] += 1 # add 1 opportunity in late position
			cbp[1][aggressorIdx] += 1 # add 1 c-bet "

	elif str.find('checks') != -1: # agggressor has had the opportunity to c-bet but did not
		
		if aggressorPosition == 'early': cbp[2][aggressorIdx] += 1 # add 1 opportunity in early position
		else:                            cbp[3][aggressorIdx] += 1 # add 1 opportunity in late position

	else: # aggressor calls, raises, or folds
		pass # no opportunity to c-bet, player in front donked. *Assumes aggressor doesn't fold a free check*
