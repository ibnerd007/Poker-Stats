from getID import *
from search import *

def calcTBP(tbID, tbp, playerIDs, currPlayerIDs):

	i = search(currPlayerIDs, tbID) # for finding position ONLY
	j = search(playerIDs, tbID) # for adding whole stat

	position = currPlayerIDs[2][i] # 'early' or 'late'

	if position == 'early' and tbp[2][j] == 0:
		tbp[0][j] += 1

	elif tbp[2][j] == 0: # late position, no tbp added previously
		tbp[1][j] += 1

	tbp[2][j] = 1 # already added, don't add 3 bet again for that person until next hand