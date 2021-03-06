import os, time

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
	window.title('PokerStats')
	window.configure(background=bg)

	photo = PhotoImage(file = "aces.png")
	window.iconphoto(True, photo)

	# Adjust size
	window.geometry("500x460")

	# Now that variables are defined, run Poker Stats
	def runPokerStats():
		spaces = ('       ','            ','  ') # cop-out way to line up output text

		status1.configure(state=NORMAL)
		status1.delete('1.0', 'end') # Delete previous output for new run
		status1.configure(state=DISABLED) # Don't allow user to change output

		date = clicked.get()
		date = date.replace('/', '') # remove slashes to make filename readable

		includeCMDnl = checkVar2.get() # set CMD option
		includeCMDplo = checkVar3.get()
		includeCMDcombined = checkVar4.get()

		includeCMD = {'NL': includeCMDnl, 'PLO': includeCMDplo, 'combined': includeCMDcombined}

		start = time.time()

		pokerStats(date, 'NL', includeCMD)
		pokerStats(date, 'PLO', includeCMD)
		output = pokerStats(date, 'combined', includeCMD) # shows every player and every hand type

		end = time.time()
		elapsed = end - start

		status1.configure(state=NORMAL)
		status1.insert(END, 'Session date:{}{}\n\n'.format(spaces[0], output[0]))

		status1.insert(END, 'Players:{}'.format(spaces[1]))
		for player in output[1]:
			status1.insert(END, '{}, '.format(player))
		status1.delete('end-3c', 'end') # Delete last comma ',' from the list of players
		status1.insert(END, '\n\n')

		status1.insert(END, 'Poker type played:{}{}'.format(spaces[2], output[2]))
		status1.configure(state=DISABLED)

		statusMessage.set('Task completed in {:.2f} seconds.'.format(elapsed))


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

	def key_pressed(event):
		if event.keysym == 'Return': runPokerStats()
		if event.keysym == 'Escape': window.destroy()

	def openStats():
		# Run command to open Excel in command line
		os.system(r"start excel.exe C:\Users\scott\OneDrive\Documents\GitHub\Poker-Stats\Outputs\stats.xlsx")

	def openNet():
		# Run command to open Excel in command line
		os.system(r"start excel.exe C:\Users\scott\OneDrive\Documents\GitHub\Poker-Stats\Outputs\net_over_time_avg.xlsx")



	# Dropdown menu options
	logs = os.listdir('Logs')
	options = [''] * len(logs) # initialize list
	for i, name in enumerate(logs): # get logs in directory
		month = name[4:6 ]
		day =   name[6:8 ]
		year =  name[8:10]
		options[i] = '{}/{}/{}'.format(month, day, year)

	# datatype of menu text
	clicked = StringVar()

	# initial menu text
	clicked.set(options[-1]) # set to penultimate element (most recent date) in list

	# Create welcome Label
	welcome = Label( window , text = "Welcome to PokerStats!", font='Arial 14', bg=bg )
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

	status1 = Text(window, height=6, wrap=WORD, bg=bg)
	status1.pack(padx=10)

	# font=TkDefaultFont

	statusMessage = StringVar()
	status2 = Label(window, textvariable=statusMessage, height=2, fg='dark green', bg=bg, font='TkDefaultFont 10')
	status2.pack(pady=1)

	# Open stats.xlsx when button is pressed
	button1 = Button( window , text = "Open this session's stats", command = openStats ).pack(pady=3)
	
	button2 = Button( window , text = "Open net vs time", command = openNet ).pack()

	window.bind('<Key>', key_pressed)

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
