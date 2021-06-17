import os

from poker_stats import pokerStats
from tkinter import *

# date = '061021'
# handTypeDesired = 'combined'

handTypes = ('combined', 'NL', 'PLO')

# Run in CMD ------------------------------------------------------------------

# date = input('Enter date:')
# handType = input('Enter poker type: (NL or PLO)')

# pokerStats(date, handType)

# input('Press enter to exit.')

# -----------------------------------------------------------------------------


def run():
	# Create object
	window = Tk()

	# Adjust size
	window.geometry("400x400")

	# Now that variables are defined, run Poker Stats
	def runPokerStats():
		date = clicked.get()
		date = date.replace('/', '') # remove slashes to make filename readable
		pokerStats(date, 'combined')

	def setState(): # disabled hand types if CMD output not wanted

		if check2['state'] == DISABLED:
			check2.config(state=NORMAL)
		else:
			check2.deselect()
			check2.config(state=DISABLED)

	# Dropdown menu options
	logs = os.listdir('Logs')
	options = [''] * len(logs) # initialize list
	for i, name in enumerate(logs): # get logs in directory
		options[i] = '{}/{}/{}'.format(name[4:6], name[6:8], name[8:10])

	# datatype of menu text
	clicked = StringVar()

	# initial menu text
	clicked.set(options[-1]) # set to penultimate element (most recent date) in list

	# Create Dropdown menu
	drop = OptionMenu( window , clicked , *options )
	drop.pack()

	checkVar1 = IntVar()
	checkVar2 = IntVar()

	check1 = Checkbutton(window, text = 'Include command line output?', variable=checkVar1, command=setState)
	check1.pack()

	check2 = Checkbutton(window, text = 'NL Texas Hold\'em', variable = checkVar2, state=DISABLED)
	check2.pack()

	# Create button, it will change label text
	button = Button( window , text = "Run" , command = runPokerStats ).pack()

	# Create Label
	label = Label( window , text = " " )
	label.pack()

	# Execute tkinter
	window.mainloop()



run()