import os

from poker_stats import pokerStats
from tkinter import *

handTypes = ('combined', 'NL', 'PLO')

# Run in CMD ------------------------------------------------------------------

# date = input('Enter date:')
# handType = input('Enter poker type: (NL or PLO)')

# pokerStats(date, handType)

# input('Press enter to exit.')

# -----------------------------------------------------------------------------


def run():
	bg = 'light blue'

	# Create object
	window = Tk()
	window.title('PokerNow Stats')
	window.configure(background=bg)

	# Adjust size
	# window.geometry("500x400")

	# Now that variables are defined, run Poker Stats
	def runPokerStats():


		hide()

		date = clicked.get()
		date = date.replace('/', '') # remove slashes to make filename readable

		includeCMDnl = checkVar2.get() # set CMD option
		includeCMDplo = checkVar3.get()
		includeCMDcombined = checkVar4.get()

		includeCMD = {'NL': includeCMDnl, 'PLO': includeCMDplo, 'combined': includeCMDcombined}

		pokerStats(         date, 'NL',       includeCMD)
		pokerStats(         date, 'PLO',      includeCMD)
		output = pokerStats(date, 'combined', includeCMD) # shows every player and every hand type

		# status1.configure(state=NORMAL)
		status1.insert(END, 'Session date: {}\n\n'.format(output[0]))
		status1.insert(END, '{}\n\n'.format(output[1]))
		status1.insert(END, output[2])
		# status1.configure(state=DISABLED)

		# status2.configure(state=NORMAL)
		status2.insert('1.0', 'Task completed successfully.')
		status2.tag_add("center", "1.0", "end")
		# status2.configure(state=DISABLED)

	def hide():
		# status1.configure(state=NORMAL)
		status1.delete('1.0', 'end') # Delete previous output for new run
		# status1.configure(state=DISABLED) # Don't allow user to change output

		# status2.configure(state=NORMAL)
		status2.delete('1.0', 'end')
		# status2.configure(state=DISABLED)



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
	welcome = Label( window , text = "Welcome to PokerNow Stats!", font='Arial 14', bg=bg )
	welcome.pack(pady=5)

	instruct = Label( window , text = "Choose your date from the dropdown below.", bg=bg )
	instruct.pack()

	# Create Dropdown menu
	drop = OptionMenu( window , clicked , *options )
	drop.pack()

	checkVar1 = IntVar()
	checkVar2 = IntVar()
	checkVar3 = IntVar()
	checkVar4 = IntVar()

	check1 = Checkbutton(window, text = 'Include command line output?', variable=checkVar1, command=setState, bg=bg,
								 activebackground=bg)
	check1.pack(pady=5)

	# The following checkbuttons allow the user to specify command line output desired.
	check2 = Checkbutton(window, text = 'NL Texas Hold\'em', variable = checkVar2, state=DISABLED, bg=bg,
								 activebackground=bg)
	check2.pack()

	check3 = Checkbutton(window, text = 'Pot Limit Omaha', variable = checkVar3, state=DISABLED, bg=bg,
								 activebackground=bg)
	check3.pack()

	check4 = Checkbutton(window, text = 'Both combined', variable = checkVar4, state=DISABLED, bg=bg,
								 activebackground=bg)
	check4.pack()

	# Call runPokerStats() when 'Run' button is pressed
	button = Button( window , text = "Run" , width=8, command = runPokerStats ).pack(pady=10)

	status1 = Text(window, height=8, wrap=WORD, bg=bg, relief=FLAT, font='TkDefaultFont')
	status1.pack(pady=5)

	status2 = Text(window, height=2, wrap=WORD, fg='dark green', bg=bg, relief=FLAT, font='TkDefaultFont')
	status2.tag_configure("center", justify='center')
	status2.pack()

	# Execute tkinter
	window.mainloop()


run()

# Run all sessions in CMD to refill averages or bankrolls ---------------------

# logs = os.listdir('Logs')
# dates = [''] * len(logs)

# for i, log in enumerate(logs):
# 	dates[i] = log[4:10]

# includeCMD = {'NL': 0, 'PLO': 0, 'combined': 0}

# for date in dates:
# 	for handType in handTypes:
# 		pokerStats(date, handType, includeCMD)
