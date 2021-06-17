import os

from poker_stats import pokerStats
from tkinter import *

handTypes = ('combined', 'NL', 'PLO')

# Run all sessions in CMD to refill averages or bankrolls ---------------------

# logs = os.listdir('Logs')
# dates = [''] * len(logs)

# for i, log in enumerate(logs):
# 	dates[i] = log[4:10]

# for date in dates:
# 	for handType in handTypes:
# 		pokerStats(date, handType, (0,0,0))

# Run in CMD ------------------------------------------------------------------

# date = input('Enter date:')
# handType = input('Enter poker type: (NL or PLO)')

# pokerStats(date, handType)

# input('Press enter to exit.')

# -----------------------------------------------------------------------------


def run():
	output0 = ''
	output1 = ''
	output2 = ''

	# Create object
	window = Tk()
	window.title('PokerNow Stats')

	# Adjust size
	window.geometry("400x400")

	# Now that variables are defined, run Poker Stats
	def runPokerStats():
		date = clicked.get()
		date = date.replace('/', '') # remove slashes to make filename readable

		includeCMDnl = checkVar2.get() # set CMD option
		includeCMDplo = checkVar3.get()
		includeCMDcombined = checkVar4.get()

		includeCMD = {'NL': includeCMDnl, 'PLO': includeCMDplo, 'combined': includeCMDcombined}

		pokerStats(date, 'NL',       includeCMD)
		pokerStats(date, 'PLO',      includeCMD)
		pokerStats(date, 'combined', includeCMD) # shows every player and every hand type

		# output0 = assignOutput(output, 0)
		# output1 = assignOutput(output, 1)
		# output2 = assignOutput(output, 2) # Outputs are various messages displayed by the GUI

	def setState(): # disabled hand types if CMD output not wanted

		if check2['state'] == DISABLED:
			check2.config(state=NORMAL)
		else:
			check2.deselect()
			check2.config(state=DISABLED)

		if check3['state'] == DISABLED:
			check3.config(state=NORMAL)
		else:
			check3.deselect()
			check3.config(state=DISABLED)

		if check4['state'] == DISABLED:
			check4.config(state=NORMAL)
		else:
			check4.deselect()
			check4.config(state=DISABLED)

	def assignOutput(output, idx):
		if idx == 0:
			output = 'This session was played on {}'.format(output[0])
		elif idx == 1:
			output = 'The following people played: {}'.format(output[1])
		elif idx == 2:
			output = '{} was/were played during the session'.format(output[2])

		return output

	# Dropdown menu options
	logs = os.listdir('Logs')
	options = [''] * len(logs) # initialize list
	for i, name in enumerate(logs): # get logs in directory
		options[i] = '{}/{}/{}'.format(name[4:6], name[6:8], name[8:10])

	# datatype of menu text
	clicked = StringVar()

	# initial menu text
	clicked.set(options[-1]) # set to penultimate element (most recent date) in list

	# Create welcome Label
	welcome = Label( window , text = "Welcome to PokerNow Stats!", font='Arial 14' )
	welcome.pack(pady=5)

	instruct = Label( window , text = "Choose your date from the dropdown below." )
	instruct.pack()

	# Create Dropdown menu
	drop = OptionMenu( window , clicked , *options )
	drop.pack()

	checkVar1 = IntVar()
	checkVar2 = IntVar()
	checkVar3 = IntVar()
	checkVar4 = IntVar()

	check1 = Checkbutton(window, text = 'Include command line output?', variable=checkVar1, command=setState)
	check1.pack(pady=5)

	# The following checkbuttons allow the user to specify command line output desired.
	check2 = Checkbutton(window, text = 'NL Texas Hold\'em', variable = checkVar2, state=DISABLED)
	check2.pack()

	check3 = Checkbutton(window, text = 'Pot Limit Omaha', variable = checkVar3, state=DISABLED)
	check3.pack()

	check4 = Checkbutton(window, text = 'Both combined', variable = checkVar4, state=DISABLED)
	check4.pack()

	# Create run button that calls runPokerStats()
	button = Button( window , text = "Run" , width=8, command = runPokerStats ).pack(pady=10)

	# status1 = Label( window , text = output0 )
	# status1.pack(pady=5)

	# status2 = Label( window , text = output1 )
	# status2.pack(pady=5)

	# status3 = Label( window , text = output2 )
	# status3.pack(pady=5)

	# Execute tkinter
	window.mainloop()



run()