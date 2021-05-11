from prettytable import PrettyTable

def printAllStats(self):
	# prints all stats for all positions in a command line table
	print('%s\'s poker statistics for this session by position\n' % self.name.upper())

	# Use prettytable

	stats = PrettyTable()

	stats.field_names = ['Stat', 'Average', 'Early', 'Late']

	stats.add_row(['VPIP', '%.1f %%' % (self.vpip[2]*100), '%.1f %%' % (self.vpip[0]*100), '%.1f %%' % (self.vpip[1]*100)])
	stats.add_row(['Pre-flop raise', '%.1f %%' % (self.pfr[2]*100), '%.1f %%' % (self.pfr[0]*100), '%.1f %%' % (self.pfr[1]*100)])
	stats.add_row(['Three-bet', '%.1f %%' % (self.tbp[2]*100), '%.1f %%' % (self.tbp[0]*100), '%.1f %%' % (self.tbp[1]*100)])
	stats.add_row(['', '', '', '']) # empty row
	stats.add_row(['Aggression factor', '%.2f' % self.af[2], '%.2f' % self.af[0], '%.2f' % self.af[1]])
	stats.add_row(['Aggression freq', '%.1f %%' % (self.afq[2]*100), '%.1f %%' % (self.afq[0]*100), '%.1f %%' % (self.afq[1]*100)])
	stats.add_row(['', '', '', '']) # empty row
	stats.add_row(['Went to showdown', '%.1f %%' % (self.wtsd[2]*100), '%.1f %%' % (self.wtsd[0]*100), '%.1f %%' % (self.wtsd[1]*100)])
	stats.add_row(['Won at showdown', '%.1f %%' % (self.wasd[2]*100), '%.1f %%' % (self.wasd[0]*100), '%.1f %%' % (self.wasd[1]*100)])

	monetaryStats = PrettyTable()
	monetaryStats.field_names = ['Monetary stats','']
	monetaryStats.add_row(['Money won at showdown', '$%.2f' % self.mwas])
	monetaryStats.add_row(['Money won before showdown', '$%.2f' % self.mwbs])

	bankrollStats = PrettyTable()
	bankrollStats.field_names = ['Bankroll', '']

	bankrollStats.add_row(['Total buy-in', '$%.2f' % self.ledger[0]])
	bankrollStats.add_row(['Total buy-out', "$%.2f" % self.ledger[1]])
	bankrollStats.add_row(['Net profit', '%s$%.2f' % (self.PoL, abs(self.ledger[2]))])
	bankrollStats.add_row(['Rebuys', self.ledger[3]])


	print(stats, '\n')
	print(monetaryStats, '\n')
	print(bankrollStats, '\n')

	# print('Bankroll')
	# print("\nTotal buy-in: $%.2f" % self.ledger[0])
	# print("Total buy-out: $%.2f" % self.ledger[1])
	# print("Net profit: %s$%.2f" % (self.PoL, abs(self.ledger[2])))
	# print("Rebuys: %d" % self.ledger[3])

