from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pandas as pd


class SentimentPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app

    def configureSentimentPage(self):
        back_b = ttk.Button(self.frame, text="Back", command= lambda: self.app.displayFrame("main frame"))
        back_b.grid(column=0, row=1, sticky=(N,S,E,W))
        #action_b = ttk.Button(freq_f, text="Run")
        #action_b.grid(column=0, row=0, sticky=(N,S,E,W))