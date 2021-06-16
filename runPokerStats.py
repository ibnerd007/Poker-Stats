import os

from poker_stats import pokerStats
from tkinter import *

date = '0610'
handTypeDesired = 'NL'

handTypes = ('combined', 'NL', 'PLO')

# date = input('Enter date:')
# handType = input('Enter poker type: (NL or PLO)')

# pokerStats(date, handType)

# input('Press enter to exit.')

def run():

	# Create object
	window = Tk()

	# Adjust size
	window.geometry("400x400")

	# Now that variables are defined, run Poker Stats
	def runPokerStats():
		date = clicked.get()
		pokerStats(date, 'NL')

	# Dropdown menu options
	logs = os.listdir('Logs')
	options = [
	"Monday",
	"Tuesday",
	"Wednesday",
	"Thursday",
	"Friday",
	"Saturday",
	"Sunday"
	]

	# datatype of menu text
	clicked = StringVar()

	# initial menu text
	clicked.set(options[-1]) # set to penultimate element (most recent date) in list

	# Create Dropdown menu
	drop = OptionMenu( window , clicked , *options )
	drop.pack()

	# Create button, it will change label text
	button = Button( window , text = "Run" , command = runPokerStats ).pack()

	# Create Label
	label = Label( window , text = " " )
	label.pack()

	# Execute tkinter
	window.mainloop()



run()