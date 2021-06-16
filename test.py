# Import module
from tkinter import *

# Create object
root = Tk()

# Adjust size
root.geometry( "200x200" )

# Change the label text
def show():
    label.config( text = clicked.get() )

# Dropdown menu options
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
clicked.set( "Monday" )

# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )
drop.pack()

# Create button, it will change label text
button = Button( root , text = "click Me" , command = show ).pack()

# Create Label
label = Label( root , text = " " )
label.pack()

# Execute tkinter
root.mainloop()

# from tkinter import *

# top = Tk()
# CheckVar1 = IntVar()
# CheckVar2 = IntVar()
# C1 = Checkbutton(top, text = "Music", variable = CheckVar1, \
#                  onvalue = 1, offvalue = 0, height=5, \
#                  width = 20)
# C2 = Checkbutton(top, text = "Video", variable = CheckVar2, \
#                  onvalue = 1, offvalue = 0, height=5, \
#                  width = 20)
# C1.pack()
# C2.pack()
# top.mainloop()
