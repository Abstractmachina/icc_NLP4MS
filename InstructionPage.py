from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
 
 
"""
Class for the Instruction Page
"""
 
class InstructionPage:
 
    def __init__(self):
 
        info = Toplevel()
        info.title("Instructions Page")
        info.geometry("900x640+0+0")
        info.columnconfigure(0, weight=1)
        info.rowconfigure(0, weight=1)
 
        major_title=('Calibri (Body)',24,'bold')
        small_title=('Calibri (Body', 20, 'bold')
        normal_text = ('Calibri (Body', 16)
 
        textTitle=Label(info, anchor = CENTER, text='Instructions\n')
        textTitle.config(font=major_title)
        textTitle.grid(row=0,column=0)
 
        instructions = Label(info, anchor=W, justify=LEFT, text=
        "This software contains tools to analyse textual data in csv files, with a particular focus on\n medical free-text entries of patients.\n"
        '1. Click on Open CSV \n'
        '2. Use the Drop Down Menu to select each value \n')
        instructions.config(font = normal_text)
        instructions.grid(row=1,column=0)

        empty_space = Label(info,text= " ")
        empty_space.grid(row=2, rowspan=8,column=0)