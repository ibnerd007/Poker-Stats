from search import *
from prettytable import PrettyTable

def printAllStatsForAllPlayers(vpipM, pfrM, tbpM, cbpM, cbpCountM, afM, afqM, wtsdM, wasdM, mwas, mwbs,
							   ledgerM, playerDict, playerIDs, handsPlayed, bestHandsM):
	# prints all stats for all players in the session to the command line using prettytable
	# Copy and paste command line output to a text file to save
	
	for i in range(len(playerIDs)):

		print('%s\'s poker statistics for this session by position\n' % playerDict[playerIDs[i]].upper())

		# Use prettytable

		stats = PrettyTable()

		stats.field_names = ['{:s}\'s stats'.format(playerDict[playerIDs[i]]), 'Average', 'Early', 'Late']

		stats.add_row(['VPIP', '{:.1f} %'.format(vpipM[i][2]*100), '{:.1f} %'.format(vpipM[i][0]*100), '{:.1f} %'.format(vpipM[i][1]*100)])
		stats.add_row(['Pre-flop raise', '{:.1f} %'.format(pfrM[i][2]*100), '{:.1f} %'.format(pfrM[i][0]*100), '{:.1f} %'.format(pfrM[i][1]*100)])
		stats.add_row(['3-bet', '{:.1f} %'.format(tbpM[i][2]*100), '{:.1f} %'.format(tbpM[i][0]*100), '{:.1f} %'.format(tbpM[i][1]*100)])

		stats.add_row(['', '', '', '']) # empty row

		stats.add_row(['Aggression factor', '{:.2f}'.format(afM[i][2]), '{:.2f}'.format(afM[i][0]), '{:.2f}'.format(afM[i][1])])
		stats.add_row(['Aggression freq', '{:.1f} %'.format(afqM[i][2]*100), '{:.1f} %'.format(afqM[i][0]*100), '{:.1f} %'.format(afqM[i][1]*100)])

		stats.add_row(['', '', '', '']) # empty row

		stats.add_row(['C-bets/opportunities', '{}/{}'.format((cbpCountM[i][0]+cbpCountM[i][1]), (cbpCountM[i][2]+cbpCountM[i][3])), 
										       '{}/{}'.format(cbpCountM[i][0], cbpCountM[i][2]),
									           '{}/{}'.format(cbpCountM[i][1], cbpCountM[i][3])])

		stats.add_row(['C-bet %', '{:.1f} %'.format(cbpM[i][2]*100), '{:.1f} %'.format(cbpM[i][0]*100), '{:.1f} %'.format(cbpM[i][1]*100)])

		stats.add_row(['', '', '', '']) # empty row

		stats.add_row(['Went to showdown', '{:.1f} %'.format(wtsdM[i][2]*100), '{:.1f} %'.format(wtsdM[i][0]*100), '{:.1f} %'.format(wtsdM[i][1]*100)])
		stats.add_row(['Won at showdown', '{:.1f} %'.format(wasdM[i][2]*100), '{:.1f} %'.format(wasdM[i][0]*100), '{:.1f} %'.format(wasdM[i][1]*100)])

		monetaryStats = PrettyTable()
		monetaryStats.field_names = ['{:s}\'s monetary stats'.format(playerDict[playerIDs[i]]),'']
		monetaryStats.add_row(['Money won at showdown', '${:.2f}'.format(mwas[i])])
		monetaryStats.add_row(['Money won before showdown', '${:.2f}'.format(mwbs[i])])

		bankrollStats = PrettyTable()
		bankrollStats.field_names = ['{:s}\'s Bankroll'.format(playerDict[playerIDs[i]]), '']

		bankrollStats.add_row(['Total buy-in', '$%.2f' % ledgerM[i][0]])
		bankrollStats.add_row(['Total buy-out', "$%.2f" % ledgerM[i][1]])

		if ledgerM[i][2] > 0: # profit
			bankrollStats.add_row(['Net profit', '+$%.2f' % abs(ledgerM[i][2])])
		else: # loss
			bankrollStats.add_row(['Net profit', '-$%.2f' % abs(ledgerM[i][2])])

		bankrollStats.add_row(['Rebuys', ledgerM[i][3]])


		print(stats, '\n')
		print(monetaryStats, '\n')
		print('*Bankroll stats are across all poker types for the session*')
		print(bankrollStats, '\n\n')
		totalPlayedbyPlayer = handsPlayed[0][i]+handsPlayed[1][i]
		print('%s played %d hands this session.' % (playerDict[playerIDs[i]], totalPlayedbyPlayer))
		# print('Best hand: %s - %s' % (bestHandsM[i][0], bestHandsM[i][2]))

		print('----------------------------------------------------------------------\n')