from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from numpy import imag

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
        ############# Configure Frame ##############################################
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure(0,weight=1)
        self.frame.columnconfigure(2,weight=1)
        style = ttk.Style()
        style.configure("MainMenu.TFrame",background="white")
        self.frame.config(style="MainMenu.TFrame")

        ############# Configure Title ##################################################
        title = Label(self.frame, background="white", text="Select an analysis tool to use",justify =CENTER,font=("bold",25,"underline"))
        title.grid(column=1,row=0)

        ############# Configure Buttons ################################################
        try:
            chart = PhotoImage(file="images\\chart.png")
            magnifying_glass = PhotoImage(file="images\\magnifying glass.png")
            user = PhotoImage(file="images\\user.png")
            trend = PhotoImage(file="images\\trend.png")
        except:
            chart = PhotoImage(file="images/chart.png")
            magnifying_glass = PhotoImage(file="images/magnifying glass.png")
            user = PhotoImage(file="images/user.png")
            trend = PhotoImage(file="images/trend.png")
            
        freq_b = Button(self.frame, text="Word Frequency Analysis       ", command=self.freq_page.validateAndInit,
                            image=chart, compound= RIGHT, font=("bold", 12), bg="light blue",borderwidth=2)
        freq_b.image = chart
        freq_b.grid(column=1,row=1,sticky=(N,S,E,W),padx=10,pady=10)

        
        search_b = Button(self.frame, text="Search the free text              ", font=("bold",12), image = magnifying_glass, compound= RIGHT,
                            bg="light blue",borderwidth=2,command=self.search_page.validateAndInit)
        search_b.image = magnifying_glass
        search_b.grid(column=1,row=2,sticky=(N,S,E,W),padx=10,pady=10)
        
        
        sentiment_b = Button(self.frame, text="User Analysis                      ", image=user,bg="light blue",borderwidth=2, 
                                 compound= RIGHT, font=("bold", 12), command= self.sent_page.validateAndInit)
        sentiment_b.image = user
        sentiment_b.grid(column=1,row=3,sticky=(N,S,E,W),padx=10,pady=10)
        
        
        trend_b = Button(self.frame, text="Trend Analysis                 ", image=trend, bg="light blue",
                              borderwidth=2, compound= RIGHT, font=("bold", 12),command= self.trend_page.validateAndInit)
        trend_b.image = trend
        trend_b.grid(column=1,row=4,sticky=(N,S,E,W),padx=10,pady=10)

        # Back button #
        back_b = Button(self.frame, bg = "light blue", borderwidth=2, font=("bold", 12), 
                            text = "Back", 
                            command = lambda: self.app.displayFrame("choose headers"))
        back_b.grid(column = 1, row = 5, sticky = (N,S,E,W),padx=10,pady=10)
        
        # Home button #
        home_b = Button(self.frame, bg = "light blue", borderwidth=2, font=("bold", 12),
                            text = "Home", 
                            command = lambda: self.app.displayFrame("home frame"))
        home_b.grid(column = 1, row = 6, sticky = (N,S,E,W),padx=10,pady=10)