# import os
from isMatch import *

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

	trackedIDs = []
	trackedNames = []

	# filenames = os.listdir('Tracked Players') # out of order, must code manually
	filenames = ['Fish_IDs.txt', 'Fish_names.txt', 'Raymond_IDs.txt', 'Raymond_names.txt', 
	             'Scott_IDs.txt', 'Scott_names.txt', 'Cedric_IDs.txt', 'Cedric_names.txt']

	# 1. Get IDs & names from files -------------------------------------------

	for i, filename in enumerate(filenames): # Go through all files with names and IDs
	    temp = list()

	    file = open(r'Tracked Players\{}'.format(filename), 'r')
	    for line in file:
	        line = line.replace('\n', '')
	        temp.append(line)

	    if i % 2 == 0: # file is even, is an ID file
	        trackedIDs.append(temp)
	    else:          # file is odd, it is a name file
	        trackedNames.append(temp)

	    file.close()

	# 2. Map indices ----------------------------------------------------------

	numPlayers = len(playerIDs)
	mappedIndices = [-1] * 4 
	newIDs = [''] * 4 # Any new IDs that are found must be stored

	for pI, tuple in enumerate(trackedIDs):
	    for trackedID in tuple:
	        for i, ID in enumerate(playerIDs):
	            if trackedID == ID:
	                # Add index to mappedIndices
	                mappedIndices[pI] = i

	# print(mappedIndices)

	# Iterate through indices. If -1, start matching
	for i, index in enumerate(mappedIndices):
	    if index == -1: # No match found above
	        # First, get list of tracked names
	        for trackedName in trackedNames[i]:
	            for j, name in enumerate(playerNames):
	                if isMatch(name, trackedName):
	                    # Found it!
	                    mappedIndices[i] = j
	                    newIDs[i] = playerIDs[j]

	# print(mappedIndices)
	# print(newIDs)

	# 3. Write new IDs to correct file -----------------------------------------
	mynames = ('Fish', 'Raymond', 'Scott', 'Cedric')

	for i, newID in enumerate(newIDs):
	    if newID != '':
	        file = open(r'Tracked Players\{}_IDs.txt'.format(mynames[i]), 'a')
	        file.write('{}\n'.format(newID))
	        file.close()

	return mappedIndices


    

	

