from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from click import command

import pandas as pd

from SentimentAnalyzer import SentimentAnalyzer


class SentimentPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app
        self.configureSentimentPage()

    def configureSentimentPage(self):
        ########################################################################
        #Header Frame
        ########################################################################
        f_header = ttk.Frame(self.frame, height = 30)
        f_header.grid(column =0, row = 0)
        l_pageTitle = ttk.Label(f_header, text ="USER ANALYSIS")
        l_pageTitle.grid(column=0,row=0)
        
        ########################################################################
        #Control frame
        ########################################################################
        f_controls = ttk.Frame(self.frame)
        f_controls.grid(column=0, row = 1, sticky = (N,S))
        
        
        ##search area
        f2_search = ttk.Frame(f_controls)
        f2_search.grid(row = 0)
        l_searchInstructions = ttk.Label(f2_search, text= "Enter User ID")
        l_searchInstructions.grid(row=0)
        
        search_phrase = StringVar(value = "Enter User ID Here")
        search_box = ttk.Entry(f2_search,textvariable=search_phrase)
        search_box.grid(row=1)
        
        b_generate = ttk.Button(f2_search, text = "Generate", 
                                command = lambda: self.generate())
        b_generate.grid(row = 2)
        
        
        ##options frame
        
        
        f2_options = ttk.Frame(f_controls)
        f2_options.grid(row =2)
        
        l_options = ttk.Label(f2_options, text = "Options")
        l_options.grid(row = 0)
        
        self.sa_on = IntVar()
        check_sa = ttk.Checkbutton(f2_options, text = "Sentiment Analysis", variable=self.sa_on)
        check_sa.grid(row = 1)
        
        self.disabl_on = IntVar()
        check_disabl = ttk.Checkbutton(f2_options, text = "Disability Score (EDSS)", variable=self.disabl_on)
        check_disabl.grid(row = 2)
        
        self.anx_on = IntVar()
        check_anx = ttk.Checkbutton(f2_options, text = "Anxiety Score (HADS)", variable=self.anx_on)
        check_anx.grid(row = 3)
        
        self.combine_on = IntVar()
        check_combine = ttk.Checkbutton(f2_options, text = "Combine", variable=self.combine_on)
        check_combine.grid(row = 4)
        
        
        ##free text options
        f2_freeText_options = ttk.Frame(f_controls)
        f2_freeText_options.grid(row = 3)
        
        self.freetxt_on = IntVar()
        ch_freetxt = ttk.Checkbutton(f2_freeText_options, text = "List Free Text", variable= self.freetxt_on)
        ch_freetxt.grid(row = 0)
        
        
        ##control footer frame
        f2_footer = ttk.Frame(f_controls)
        f2_footer.grid(row = 4)
        
        b_download = ttk.Button(f2_footer, text="Download")
        b_download.grid(row=0, sticky=(N,S,E,W))
        b_back = ttk.Button(f2_footer, text="Back", 
                            command= lambda: self.app.displayFrame("main frame"))
        b_back.grid(row=1, sticky=(N,S,E,W))
        
        
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
        
        return
        
        
    def generate(self) :
        """
        print ("generating")
        print("Options:")
        print(f"Sentiment Analysis: {self.sa_on.get()}")
        print(f"Disability Score: {self.disabl_on.get()}")
        print(f"Anxiety Score: {self.anx_on.get()}")
        print(f"combine: {self.combine_on.get()}")
        print(f"free text: {self.freetxt_on.get()}")
        """
        analyzer = SentimentAnalyzer()
        analyzer.buildSentimentHistory()
        
        return