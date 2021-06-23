def assignDealer(str):
	# save dealer ID in temp variable
	atIndex = str.find('@')

	dealerID = str[atIndex+2:atIndex+2+10] # 10 character player ID

	return dealerID