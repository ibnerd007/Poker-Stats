def whichHandType(str, handType):
	# Returns which hand type is being played now: Hold em or PLO

	if str.find('No Limit Texas Hold\'em') != -1: # This hand is NL Holdem
		handType = 'NL'
	elif str.find('Pot Limit Omaha Hi') != -1: # This hand is PLO
		handType = 'PLO'
	assert handType != None, 'Something is wrong, there should be hand type'

	return handType