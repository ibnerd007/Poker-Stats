from search import *

def calcMWAS(mwas, pot, winnerID, playerIDs):
	i = search(playerIDs, winnerID)
	print('Pot size:',pot)
	mwas[i] += pot # add money won at showdown, in dollars & cents