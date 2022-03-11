from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pandas as pd

from FrequencyPage import FrequencyPage
from SearchPage import SearchPage
from SentimentPage import SentimentPage



class MainMenu:
    
    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame    
        self.app = app

        self.freq_page = FrequencyPage(self.root,self.app.addPageFrame("freq frame",self.root),self.app)
        self.search_page = SearchPage(self.root,self.app.addPageFrame("search frame",self.root),self.app)
        self.sent_page = SentimentPage(self.root,self.app.addPageFrame("sent frame",self.root),self.app)     

        self.configureMainMenu()

        

    def configureMainMenu(self):

        """
        Configures the layout of the main menu of our program
        which is what the user sees after selecting the csv file and pressing next

        """

        ############# Configure Buttons ################################################
        freq_b = ttk.Button(self.frame, text="Word Frequency Analysis", command= lambda: self.app.displayFrame("freq frame"))
        freq_b.grid(column=0,row=0,sticky=(N,S,E,W))

        search_b = ttk.Button(self.frame, text="Search the free text", command=self.search_page.searchEntryButtonClick)
        search_b.grid(column=0,row=1,sticky=(N,S,E,W))
        
        sentiment_b = ttk.Button(self.frame, text="User Analysis", command= lambda: self.app.displayFrame("sent frame"))
        sentiment_b.grid(column=0,row=2,sticky=(N,S,E,W))

        back_b = ttk.Button(self.frame, text="Back", command= lambda: self.app.displayFrame("home frame"))
        back_b.grid(column=0, row=3, sticky=(N,S,E,W))