def replaceSuits(str):
	# Replaces random characters imported into Excel with correct suits in string str

	# str = str.replace('â™¥', '♥️')
	# str = str.replace('â™¦', '♦')
	# str = str.replace('â™£', '♣')
	# str = str.replace('â™ ', '♠')

	str = str.replace('â™¥', 'h')
	str = str.replace('â™¦', 'd')
	str = str.replace('â™£', 'c')
	str = str.replace('â™ ', 's')

	return str
