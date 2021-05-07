def startingHandNumber(str):
	# save dealer ID in temp variable
	atIndex = str.find('@')
	if (atIndex == -1):
		assert("Issue")
	dealerID = str[atIndex+2:atIndex+2+10] # 10 character player ID
	return dealerID