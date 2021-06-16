# Python program to explain os.getcwd() method
		
# importing os module
import os
	
# Get the current working
# directory (CWD)
list = os.listdir('Ledgers - Copy')
	
# Print the current working
# directory (CWD)
print("Files in directory:", list)

# Rename the files, adding '21' for the year '2021' to all the files present

def renameFiles():
	working_dir = 'Ledgers - Copy'
	for filename in os.listdir('Ledgers - Copy'):

		src = os.path.join(working_dir, filename)
		dst = os.path.join(working_dir, filename[:11] + '21' + filename[11:])

		os.rename(src, dst)

renameFiles()

list = os.listdir('Ledgers - Copy')
print("Files in directory:", list)


