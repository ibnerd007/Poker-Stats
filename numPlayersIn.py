def numPlayersIn(list):
	# Checks list to see if any other indices besides the one given as an argument
	# are not zero. Used to scan the list for other players that are still in at
	# showdown.
	playersIn = 0
	for i in range(len(list)):
		if list[i] == 0: # player is still in
			playersIn += 1

	return playersIn