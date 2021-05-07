from search import *

def calcMWAS(mwas, pot, winnerID, playerIDs):
	i = search(playerIDs, winnerID)
	mwas[i] += pot # add money won at showdown, in dollars & cents