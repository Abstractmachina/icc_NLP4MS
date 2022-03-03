# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from tkinter import *
from tkinter import ttk

data_dict = {'ID': [1, 2, 3, 4, 5], 'free_text': 
             ['my leg has been hurting', 
              'i can\'t sleep',
              'a year ago it was much worse',
              'it was difficult having covid'
              ]}

data_frame = pd.DataFrame(data=data_dict)

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()