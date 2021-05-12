def replaceSuits(str):
	# Replaces random characters imported into Excel with correct suits in string str

	str = str.replace('â™¥', '♥️')
	str = str.replace('â™¦', '♦')
	str = str.replace('â™£', '♣')
	str = str.replace('â™ ', '♠')

	return str
