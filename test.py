import re

input_name = 'dricec'

pattern = '[eric]'

if re.search(pattern, input_name):
    print('Nice')
else: 
    print('Nope')

print('Return value:', re.search(pattern, input_name))

print(re.findall(pattern, input_name))