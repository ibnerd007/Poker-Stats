from howManyTens import *
from search import *
from replaceSuits import *

def calcBestHands(str, wI, bestHands):

	hands = ['Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 
			 'Four of a Kind', 'Straight Flush', 'Royal Flush']
	cardOrder = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

	tempStr = str[str.find('with'):] # Truncate string to only include parts about winning hand
	handStr = replaceSuits(tempStr) # Suits come into Excel incorrectly. This function corrects them

	currIndex = bestHands[1][wI] # bestHands[1][wI*] = rank, *winner index
	newIndex = -1 # reset index

	for j in range(len(hands)):

		if handStr.find(hands[j]) != -1: # the winning hand has been identified
			# first, capture the high card, two characters if high card is a 10
			tenHigh = howManyTens(handStr[handStr.find('combination: ') + 13:handStr.find('combination: ') + 15])
			highCard = handStr[handStr.find('combination') + 13:
							   handStr.find('combination') + 14 + tenHigh]
	
			# Need to code some exceptions
			if hands[j] == 'Pair' and handStr.find('Two') != -1: # hand is actually two pair
				newIndex = 1 # index for two pair

			elif hands[j] == 'Flush':
				if handStr.find('Straight') != -1:
					newIndex = 7 # index for straight flush
				elif handStr.find('Royal') != -1:
					newIndex = 8 # index for royal flush
				else:
					newIndex = 4

			else: # just set the new index = j
				newIndex = j

		if (newIndex != -1 and newIndex > currIndex) or \
		   (newIndex == currIndex and search(cardOrder, highCard) > search(cardOrder, bestHands[3][wI])): # better hand OR better high card
				bestHands[0][wI] = hands[newIndex] # hand type, string
				bestHands[1][wI] = newIndex # new best hand ranking, for later comparison

				# Add hand combination for reporting later
				bestHands[2][wI] = handStr[handStr.find('combination: ') + 13: handStr.find(')')]
				bestHands[3][wI] = highCard # store high card for later comparison

				break # no need to continue checking if hand is better through the rest of hands[]