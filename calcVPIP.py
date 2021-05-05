from appendMultiple import *
from getID import *
from search import *

def calcVPIP(str, vpip, playerIDs, currPlayerIDs):
	# Every hand, looks for players that call or raise preflop

	# Find ID of player
	vpipID = getID(str)
	i = search(currPlayerIDs, vpipID) # for finding position ONLY
	j = search(playerIDs, vpipID) # for adding whole stat

	position = currPlayerIDs[2][i] # 'early' or 'late'

	if position == 'early' and vpip[2][j] == 0:
		vpip[0][j] += 1
	elif vpip[2][j] == 0: # late position, no vpip added previously
		vpip[1][j] += 1

	vpip[2][j] = 1 # already added, don't add call or raise again until next hand


