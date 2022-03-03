# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

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