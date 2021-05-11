def reportPercentages(self, position, i):

	print(self.name.upper(), '\n')

	if position == '': # stat averages have been requested
		print('stat averages                    Bankroll stats')
	else:
		print('%s stats                      Bankroll stats' % position)

	# stat indexes indicate position: early, late, or average
	print("VPIP             : %.1f %%        Total buy-in: $%.2f" % ((self.vpip[i]*100), self.ledger[0]))
	print("Pre-flop raise   : %.2f %%       Total buy-out: $%.2f" % ((self.pfr[i]*100), self.ledger[1]))
	print("Three-bet        : %.2f %%        Net profit: %s$%.2f" % ((self.tbp[i]*100), self.PoL, abs(self.ledger[2])))
	print("                                 Rebuys: %d" % self.ledger[3])

	print("\nAggression factor:", self.af[i])

	print("Aggression freq  : %.1f %%" % (self.afq[i]*100))
	print("\nWent to showdown  : %.1f %% of hands played" % (self.wtsd[i]*100))
	print("Won at showdown   : %.1f %% \"" % (self.wasd[i]*100))

	print("\nMonetary stats for %s, not position-based" % self.name)
	print("$ won at showdown    : $%.2f" % self.mwas)
	print("$ won before showdown: $%.2f" % self.mwbs)