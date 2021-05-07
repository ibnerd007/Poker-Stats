from search import *

def calcMWBS(mwbs, pot, winnerID, playerIDs):
	i = search(playerIDs, winnerID)
	mwbs[i] += pot # add money won before showdown, in dollars & cents