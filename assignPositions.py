from search import *

def assignPositions(str, dealerID, playerIDs, currPlayerIDs, handsPlayed):
	# Assigns new players an index, seat, and position
	# Assigns old players a seat and position

	# Start by assigning new players to an index
	playersAdded = 0 # so we know how to append the stats lists

	prevAtIndex = 0

	while str.find('@', prevAtIndex+1) != -1: # while another player ID can still be found,
		# add new players to list

		atIndex = str.find('@', prevAtIndex+1) # find next @ symbol before ID
		tempID = str[atIndex+2:atIndex+2+10] # 10 character player ID

		currPlayerIDs[0].append(tempID) # add player ID to list for this hand
		
		if search(playerIDs, tempID) == -1: # new player has been found
			playerIDs.append(tempID) # add new player ID to main list
			handsPlayed.append(0)
			playersAdded += 1

		handsPlayed[search(playerIDs, tempID)] += 1 # another hand is played

		prevAtIndex = atIndex # hold past index to make sure to find new @ symbol
	# ---------------------------------------------------------------------------------------

	# Next, assign each player to a seat.
	prevSeatIndex = 0

	while str.find('#', prevSeatIndex+1) != -1:

		seatIndex = str.find('#',prevSeatIndex+1) + 1 # find number that shows seat
		seat = int(str[seatIndex:seatIndex+2]) # assign seat index

		currPlayerIDs[1].append(seat)

		prevSeatIndex = seatIndex # hold past index to make sure to find new "#" symbol

	# ---------------------------------------------------------------------------------------

	# Assign positions for the hand
	dealerIndex = search(currPlayerIDs[0],dealerID)

	# i = 0
	for i in range(len(currPlayerIDs[1])):
		currPlayerIDs[2].append(0) # preallocate space for positions
		

	for j in range(len(currPlayerIDs[1])): # loop through seat numbers
		currPlayerIDs[2][(dealerIndex+j) % len(currPlayerIDs[1])] = j # fill positions, wrap around list

	# print(currPlayerIDs) # Use to see actual positions rather than early/late

	#----------------------------------------------------------------------------------------

	# Determine whether position is early or late
	for i in range(len(currPlayerIDs[2])):
		if currPlayerIDs[2][i]/len(currPlayerIDs[2]) < 0.5:
			currPlayerIDs[2][i] = 'late' # player is in early position

		else:
			currPlayerIDs[2][i] = 'early'

	return playersAdded