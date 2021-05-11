def reportDecimals(self, position, i):

	print(self.name.upper(), '\n')

	if position == '': # stat averages have been requested
		print('stat averages                  Bankroll stats')
	else:
		print('%s stats for %s             Bankroll stats' % (position, self.name))

	print("VPIP             : %.2f           Total buy-in: $%.2f" % ((self.vpip[i]), self.ledger[0]))
	print("Pre-flop raise   : %.2f          Total buy-out: $%.2f" % ((self.pfr[i]), self.ledger[1]))
	print("Three-bet        : %.2f           Net profit: %s$%.2f" % ((self.tbp[i]), self.PoL, abs(self.ledger[2])))
	print("                                 Rebuys: %d" % self.ledger[3])

	print("Aggression factor:", self.af[i])
	print("Aggression freq  :", self.afq[i])

	print("\nWent to showdown  :", self.wtsd[i])
	print("Won at showdown   :", self.wasd[i])

	print("\nMonetary stats for %s, not position-based" % self.name)
	print("$ won at showdown    : $%.2f" % self.mwas)
	print("$ won before showdown: $%.2f" % self.mwbs)