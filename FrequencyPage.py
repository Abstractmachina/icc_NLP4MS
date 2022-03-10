from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pandas as pd

class FrequencyPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app

        self.configureFreqPage()
    
    def configureFreqPage(self):
        back_b = ttk.Button(self.frame, text="Back", command= lambda: self.app.displayFrame("main frame"))
        back_b.grid(column=0, row=0, sticky=(N,S,E,W))