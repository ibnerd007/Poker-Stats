from tkinter import Tk, Checkbutton, DISABLED
root = Tk()
def click():
    check.config(state=DISABLED)
check = Checkbutton(text="Click Me", command=click)
check.grid()
root.mainloop()