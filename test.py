from isMatch import *

playerIDs = ['kjrngiakur', 'aijrgbaikgr', 'uiajrngba', 'L5G0fi1P1T', '27qpPjb-rT', '-4Mt9GCcpf', 'ethbaefthbat']

playerNames = ['Ray', 'Donny', 'Dave', 'FIsh', 'Cedric', 'Scott', 'Daniel']

trackedIDs =   (('L5G0fi1P1T', 'w'), ('gpL6BdHM3Z', 'w'), ('-4Mt9GCcpf', 'X6PyKTwqmn'), ('UOl9ieuNTH', '27qpPjb-rT'))
#                 Fish                 Raymond              Scott                         Cedric

trackedNames = (('Fish', 'Howler', 'River God'), ('Ray', 'Raymond'), ('Scott', 'Scotty'), 
    ('Cedric', 'Il Magnifico'))

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


    