def assignPlayerIndices(playerIDs, playerNames):
	# Arguments: playerIDs:   current 10-digit IDs of players this session
	#            playerNames: nicknames used by the players this session.
	# Returns:   tuple of player indices for the session.

	""" Trans-session stats all commonly require that the 4 tracked players' trans-session indices
		(Fish = 0, Raymond = 1, Scott = 2, Cedric = 3) are mapped to the current session indices
		within playerIDs. Remember, playerIDs is appended according to the order in which players
		join the session.

		This function maps those indices, matching the ID in playerIDs to one of the saved IDs for the
		tracked player.

		Tracked players also may use new IDs unexpectedly, not matching any saved ID. Instead of assuming 
		the tracked player didn't play, it tries to match the player's nickname used during the session 
		(contained in playerNames) to one of the saved nicknames. These nicknames have commonly been
		used in the past.

		If it matches within a certain margin of error, it will add the player's new ID to the saved IDs
		and add the player's stats. It will also send an informational message to the GUI regarding the 
		changes.

		If neither method works, the function will make the index -1, and assume the player did not play.
	"""


	trackedIDs =   (('L5G0fi1P1T'), ('gpL6BdHM3Z'), ('-4Mt9GCcpf', 'X6PyKTwqmn'), ('UOl9ieuNTH', '27qpPjb-rT'))
	#                 Fish            Raymond         Scott                         Cedric

	trackedNames = (('Fish', 'Howler', 'River God'), ('Ray', 'Raymond'), ('Scott', 'Scotty'), 
		('Cedric', 'Il Magnifico'))

	mappedIndices = []


	for pI, tuple in trackedIDs:
		for trackedID in tuple:
			for i, ID in enumerate(playerIDs):
				if trackedID == ID:
					# Add index to mappedIndices
					mappedIndices[pI] = i

	

