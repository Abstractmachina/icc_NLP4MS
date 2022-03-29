import os

from tkinter import *
from tkinter import ttk, filedialog

import pandas as pd

from SentimentController import SentimentController


class SentimentPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app
        self.searchBox = None   #search box that contains user input
        self.displayFrame = None #frame where generated profile is displayed
        self.controller = SentimentController()
        self.controller.setUserView(self)
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
        
        ##load CSV
        f2_loadCSV = ttk.Frame(f_controls)
        f2_loadCSV.grid(row = 0)
        
        l_loadFile = ttk.Label(f2_loadCSV, text="Load CSV File")
        l_loadFile.grid(row = 0)
        b_loadFile = ttk.Button(f2_loadCSV, text = "Open File", 
                                command = lambda: self.loadFile_click())
        b_loadFile.grid(row = 1)
        
        
        ##search area
        f2_search = ttk.Frame(f_controls)
        f2_search.grid(row = 1)
        
        l_searchInstructions = ttk.Label(f2_search, text= "Enter User ID")
        l_searchInstructions.grid(row=0)
        
        search_phrase = StringVar()
        search_box = ttk.Entry(f2_search,textvariable=search_phrase)
        search_box.grid(row=1)
        self.searchBox = search_box
        
        
        ##options frame
        f2_options = ttk.Frame(f_controls)
        f2_options.grid(row =2)
        
        l_options = ttk.Label(f2_options, text = "Options")
        l_options.grid(row = 0)
        
        self.sa_on = IntVar()
        check_sa = ttk.Checkbutton(f2_options, text = "Sentiment Analysis", 
                                   variable=self.sa_on)
        check_sa.grid(row = 1)
        
        self.disabl_on = IntVar()
        check_disabl = ttk.Checkbutton(f2_options,text = "Disability Score (EDSS)", 
                                       variable=self.disabl_on)
        check_disabl.grid(row = 2)
        
        self.combine_on = IntVar()
        check_combine = ttk.Checkbutton(f2_options, text = "Combine", 
                                        variable=self.combine_on)
        check_combine.grid(row = 4)
        
        
        ##free text options
        f2_freeText_options = ttk.Frame(f_controls)
        f2_freeText_options.grid(row = 3)
        
        self.freetxt_on = IntVar()
        ch_freetxt = ttk.Checkbutton(f2_freeText_options, text = "List Free Text", 
                                     variable= self.freetxt_on)
        ch_freetxt.grid(row = 0)
        
        
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
        
    def loadFile_click(self):
        file = filedialog.askopenfile(mode="r", 
                                      filetypes=[("CSV Files", "*.csv")])
        if file:
            filepath = os.path.abspath(file.name)
            self.controller.loadCSV(filepath)
        return
        
    def generate_click(self) :
        #store entered user id
        #TODO: sanity check, only ints allowed
        userId = int(self.searchBox.get())
        self.searchBox.delete(0, "end")
        
        #clear display frame
        for widget in self.displayFrame.winfo_children():
            widget.destroy()

        #create user info header
        
        userInfo = self.controller.buildUserInfo(userId)
        r = Text(self.displayFrame, width = 95, height = 10)
        r.insert("end", userInfo)
        r.configure(font="10")
        r.configure(state= "disabled")
        r.grid(row=0, column = 0, sticky=(N,S,E,W))
        r_scroll = ttk.Scrollbar(self.displayFrame, orient=VERTICAL, command=r.yview)
        r_scroll.grid(row=0, column=1, rowspan = 1, sticky=(N,S))
        r["yscrollcommand"] = r_scroll.set
        
        self.controller.buildUserGraphs(userId, self.displayFrame, 
                                        self.sa_on, self.disabl_on,
                                        self.combine_on)
            
        #list free text
        
            
        return