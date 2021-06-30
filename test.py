# import os
from isMatch import *

playerIDs = ['kjrngiakur', 'aijrgbaikgr', 'uiajrngba', 'L5G0fi1P1T', '27qpPjb-rT', '-4Mt9GCcpf', 'ethbaefthbat']

playerNames = ['Ray', 'Donny', 'Dave', 'FIsh', 'Cedric', 'Scott', 'Daniel']

trackedIDs = []
trackedNames = []

# filenames = os.listdir('Tracked Players') # out of order, must code manually
filenames = ['Fish_IDs.txt', 'Fish_names.txt', 'Raymond_IDs.txt', 'Raymond_names.txt', 
             'Scott_IDs.txt', 'Scott_names.txt', 'Cedric_IDs.txt', 'Cedric_names.txt']

# 1. Get IDs & names from files -------------------------------------------

for i, filename in enumerate(filenames):
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

print(mappedIndices)

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

print(mappedIndices)
print(newIDs)

# 3. Write new IDs to correct file -----------------------------------------
mynames = ('Fish', 'Raymond', 'Scott', 'Cedric')

for i, newID in enumerate(newIDs):
    if newID != '':
        file = open(r'Tracked Players\{}_IDs.txt'.format(mynames[i]), 'a')
        file.write('{}\n'.format(newID))
        file.close()

# return mappedIndices


    