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
        info.geometry("900x640+500+150")
        info.columnconfigure(0, weight=1)
        info.rowconfigure(0, weight=1)
 
        major_title=('Calibri (Body)',24,'bold')
        small_title=('Calibri (Body', 20, 'bold')
        normal_text = ('Calibri (Body', 16)
 
        textTitle=Label(info, anchor = W, text='Instructions\n\n')
        textTitle.config(font=major_title)
        textTitle.pack()
 
        getting_started = Label(info, anchor = W, text=
        '1. Click on Open CSV \n'
        '2. Use the Drop Down Menu to select each value \n')
        getting_started.config(font = normal_text)
        getting_started.pack()