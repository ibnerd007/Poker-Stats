from getID import *
from search import *

def calcPFR(pfrID, pfr, playerIDs, currPlayerIDs):
	# Every hand, looks for players that call or raise preflop

	i = search(currPlayerIDs, pfrID) # for finding position ONLY
	j = search(playerIDs, pfrID) # for adding whole stat

	position = currPlayerIDs[2][i] # 'early' or 'late'

	if position == 'early' and pfr[2][j] == 0:
		pfr[0][j] += 1
	elif pfr[2][j] == 0: # late position, no pfr added previously
		pfr[1][j] += 1

	pfr[2][j] = 1 # already added, don't add call or raise again until next hand