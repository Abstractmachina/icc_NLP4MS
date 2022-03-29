from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from turtle import bgcolor

from pyparsing import col

from SentimentController import SentimentController

class TrendPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app
        self.searchBox = None   #search box that contains user input
        self.displayFrame = None #frame where generated profile is displayed
        self.controller = SentimentController()
        self.controller.setUserView(self)
        self.configureTrendPage()

        
    def configureTrendPage(self):
        ########################################################################
        #Header Frame
        ########################################################################
        headerStyle = ttk.Style()
        headerStyle.configure("header.TFrame", background = "blue")
        f_header = ttk.Frame(self.frame, style = "header.TFrame", height = 30)
        #f_header.config(bgcolor = "blue")
        f_header.grid(column =0, row = 0)
        l_pageTitle = ttk.Label(f_header, text ="TREND ANALYSIS")
        l_pageTitle.grid(column=0,row=0)
        
         ########################################################################
        #Control frame
        ########################################################################
        f_controls = ttk.Frame(self.frame)
        f_controls.grid(column=0, row = 1, sticky = (N,S))
        
        ##load CSV
        f2_loadCSV = ttk.Frame(f_controls)
        f2_loadCSV.grid(row = 0)
        
        l_loadFile = ttk.Label(f2_loadCSV, text="Load CSV File")
        l_loadFile.grid(row = 0)
        b_loadFile = ttk.Button(f2_loadCSV, text = "Open File", 
                                command = lambda: self.loadFile_click())
        b_loadFile.grid(row = 1)
               
        
        ##options frame
        f2_options = ttk.Frame(f_controls)
        f2_options.grid(row =2)
        
        l_options = ttk.Label(f2_options, text = "Options")
        l_options.grid(row = 0)
        
        l_numUsers = ttk.Label(f2_options, text = "Number of Users")
        l_numUsers.grid(row = 1, column= 0)
        
        vcmd = (self.root.register(self.isInt), '%S')
        numUsers = StringVar()
        e_numUsers = ttk.Entry(f2_options, validate="all", validatecommand=vcmd, textvariable=numUsers)
        e_numUsers.grid(row=1, column = 1)
        
        self.sa_on = IntVar()
        check_sa = ttk.Checkbutton(f2_options, text = "Sentiment Trend", 
                                   variable=self.sa_on)
        check_sa.grid(row = 2)
        
        self.disabl_on = IntVar()
        check_disabl = ttk.Checkbutton(f2_options,text = "EDSS Trend", 
                                       variable=self.disabl_on)
        check_disabl.grid(row = 3)
        
        self.combine_on = IntVar()
        check_combine = ttk.Checkbutton(f2_options, text = "Combine", 
                                        variable=self.combine_on)
        check_combine.grid(row = 4)
        
        
        l_distribution = ttk.Label(f2_options, text = "Sentiment Distribution")
        l_distribution.grid(row = 5)
        
        self.distroNeg_on = IntVar()
        check_distroNeg = ttk.Checkbutton(f2_options, text="Negative", 
                                          variable=self.distroNeg_on)
        check_distroNeg.grid(row = 6)
        
        self.distroNeu_on = IntVar()
        check_distroNeu = ttk.Checkbutton(f2_options, text="Neutral", 
                                          variable=self.distroNeu_on)
        check_distroNeu.grid(row = 7)
        
        self.distroPos_on = IntVar()
        check_distroPos = ttk.Checkbutton(f2_options, text="Positive", 
                                          variable=self.distroPos_on)
        check_distroPos.grid(row = 8)
        
        self.distroComp_on = IntVar()
        check_distroComp = ttk.Checkbutton(f2_options, text="Compound", 
                                          variable=self.distroComp_on)
        check_distroComp.grid(row = 9)
        
        self.scatter_on = IntVar()
        check_scatter = ttk.Checkbutton(f2_options, text="Scatter", 
                                          variable=self.scatter_on)
        check_scatter.grid(row = 10)
        
        
        ##control footer frame
        f2_footer = ttk.Frame(f_controls)
        f2_footer.grid(row = 4)
        
        b_generate = ttk.Button(f2_footer, text = "Generate", 
                                command = lambda: self.generate_click())
        b_generate.grid(row = 0)
        b_download = ttk.Button(f2_footer, text="Download")
        b_download.grid(row=1, sticky=(N,S,E,W))
        b_back = ttk.Button(f2_footer, text="Back", 
                            command= lambda: self.app.displayFrame("main frame"))
        b_back.grid(row=2, sticky=(N,S,E,W))
        
        
        ########################################################################
        #Display frame
        ########################################################################
        f_display = ttk.Frame(self.frame)
        f_display.grid(column = 1, row = 1, sticky=(N,S,E))
        results = Text(f_display, width=95, height=20)
        results.grid(row=0, column = 0, sticky=(N,S,E, W))
        results.insert("1.0","Result will appear here")
        results.configure(font="16")
        results.configure(state="disabled")
        self.displayFrame = f_display
        
        return
    
    def isInt(S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True
        #t3.bell() # .bell() plays that ding sound telling you there was invalid input
        return False