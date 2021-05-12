def calcBestHands(str, wI, bestHands):

	hands = ['Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 
			    'Four of a Kind', 'Straight Flush', 'Royal Flush']
	# cardOrder = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']

	handStr = str[str.find('with'):] # Truncate string to only include parts about winning hand
	currIndex = bestHands[1][wI] # rank
	newIndex = -1

	for j in range(len(hands)):

		if handStr.find(hands[j]) != -1: # the winning hand has been identified
			# Need to code some exceptions
			if hands[j] == 'Pair' and handStr.find('Two') != -1: # hand is actually two pair
				newIndex = 1 # index for two pair

			elif hands[j] == 'Flush':
				if handStr.find('Straight') != -1:
					newIndex = 7 # index for straight flush
				elif handStr.find('Royal') != -1:
					newIndex = 8 # index for royal flush

			else: # just set the new index = j
				newIndex = j

		if newIndex != -1 and newIndex >= currIndex: # a better hand has been found
			bestHands[0][wI] = hands[newIndex]
			bestHands[1][wI] = newIndex
			print(bestHands)
			break