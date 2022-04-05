from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pandas as pd

from FrequencyPage import FrequencyPage
from SearchPage import SearchPage
from SentimentPage import SentimentPage
from TrendPage import TrendPage



class MainMenu:
    
    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame    
        self.app = app

        self.freq_page = FrequencyPage(self.root,self.app.addPageFrame("freq frame",self.root),self.app)
        self.search_page = SearchPage(self.root,self.app.addPageFrame("search frame",self.root),self.app)
        self.sent_page = SentimentPage(self.root,self.app.addPageFrame("sent frame",self.root),self.app)     
        self.trend_page = TrendPage(self.root, self.app.addPageFrame("trend frame", self.root), self.app)

        self.configureMainMenu()

        

    def configureMainMenu(self):

        """
        Configures the layout of the main menu of our program
        which is what the user sees after selecting the csv file and pressing next

        """

        ############# Configure Buttons ################################################
        freq_b = ttk.Button(self.frame, text="Word Frequency Analysis", command=self.freq_page.validateAndInit)
        freq_b.grid(column=0,row=0,sticky=(N,S,E,W))

        search_b = ttk.Button(self.frame, text="Search the free text", command=self.search_page.searchEntryButtonClick)
        search_b.grid(column=0,row=1,sticky=(N,S,E,W))
        
        sentiment_b = ttk.Button(self.frame, text="User Analysis", 
                                 command= self.sent_page.validateAndInit)
        sentiment_b.grid(column=0,row=2,sticky=(N,S,E,W))
        
        trend_b = ttk.Button(self.frame, text="Trend Analysis", command= self.trend_page.validateAndInit)
        trend_b.grid(column=0,row=3,sticky=(N,S,E,W))

        # Back button #
        back_b = ttk.Button(self.frame, 
                            text = "Back", 
                            command = lambda: self.app.displayFrame("choose headers"))
        back_b.grid(column = 0, row = 4, sticky = (N,S,E,W))
        
        # Home button #
        home_b = ttk.Button(self.frame, 
                            text = "Home", 
                            command = lambda: self.app.displayFrame("home frame"))
        home_b.grid(column = 0, row = 5, sticky = (N,S,E,W))