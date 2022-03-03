from tkinter import *
from tkinter import ttk

import pandas as pd

data = ['my leg has been hurting', 
        'i can\'t sleep',
        'a year ago it was much worse',
        'it was difficult having covid',
        'the last year has been difficult as i went into relapse']


def searchData(word):
    count = 0
    for string in data:
        if (string.find(word)!=-1):
            count += 1
    return count

def displayWordCount(frm, ent):
   ttk.Label(frm, text=searchData(ent.get())).grid(column=0, row=1)

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Enter to search:").grid(column=0, row=0)
ent = ttk.Entry(root)
btn = ttk.Button(frm, text="Search", command=displayWordCount(frm, ent)).grid(column=1, row=0)
root.mainloop()



# I kept getting wierd ass errors when I tried to .pack() with the above code?
# Created a second frame to write a function to take in/print user input

second_frame= Tk()
second_frame.geometry("1000x500")

def printUserInputToScreen():
   global entry
   string= entry.get()
   label.configure(text=string)

def takeUserInput():
    global entry
    string = entry.get()
    return string

label=Label(second_frame, text="", font=("Calibri 22 bold"))
label.pack()
entry= Entry(second_frame, width= 40)
entry.focus_set()
entry.pack()
ttk.Button(second_frame, text= "Input Text then Click Me",width= 20, command= printUserInputToScreen).pack(pady=20)

second_frame.mainloop()