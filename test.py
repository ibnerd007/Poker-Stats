import regex as re

numRegex = re.findall('[0-9]+', 'collected 1176 from pot 10 high')
assert len(numRegex) >= 1, 'No number in string'
print(int(numRegex[0]))