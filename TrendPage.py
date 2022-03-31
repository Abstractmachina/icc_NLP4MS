from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk

import os


from SentimentController import SentimentController

class TrendPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app
        self.searchBox = None   #search box that contains user input
        self.displayFrame = None #frame where generated profile is displayed
        self.controller = SentimentController()
        self.configureTrendPage()

        
    def configureTrendPage(self):
        ########################################################################
        #Header Frame
        ########################################################################
        #TODO: style not working
        headerStyle = ttk.Style()
        headerStyle.configure("header.TFrame", background = "blue")
        f_header = ttk.Frame(self.frame, style = "header.TFrame", height = 30)
        f_header.grid(column =0, row = 0)
        l_pageTitle = ttk.Label(f_header, text ="TREND ANALYSIS")
        l_pageTitle.grid(column=0,row=0)
        
        #########################################################################
        #Control frame
        ########################################################################
        f_controls = ttk.Frame(self.frame)
        f_controls.grid(column=0, row = 1, sticky = (N,S))
        
        ##  load CSV
        f2_loadCSV = ttk.Frame(f_controls)
        f2_loadCSV.grid(row = 0)
        
        l_loadFile = ttk.Label(f2_loadCSV, text="Load CSV File")
        l_loadFile.grid(row = 0)
        b_loadFile = ttk.Button(f2_loadCSV, text = "Open File", 
                                command = lambda: self.loadFile_click())
        b_loadFile.grid(row = 1)
               
        
        ##  options frame
        f2_options = ttk.Frame(f_controls)
        f2_options.grid(row =2)
        
        
        ### input
        f3_input = ttk.Frame(f2_options)
        f3_input.grid(row = 0)
        
        l_options = ttk.Label(f3_input, text = "Options")
        l_options.grid(row = 0)
        
        l_numUsers = ttk.Label(f3_input, text = "Number of Users\n(0 for all)")
        l_numUsers.grid(row = 1, column= 0)
        
        numUsers = StringVar()
        self.e_numUsers = ttk.Entry(f3_input, textvariable=numUsers)
        self.e_numUsers.grid(row=1, column = 1)
        
        
        ### trend graphs
        f3_trends = ttk.Frame(f2_options)
        f3_trends.grid(row = 1)

        l_trends = ttk.Label(f3_trends, text = "Trend Graphs")
        l_trends.grid(row = 0)
        self.sa_on = IntVar()
        check_sa = ttk.Checkbutton(f3_trends, text = "Sentiment Trend", 
                                   variable=self.sa_on)
        check_sa.grid(row = 1)
        
        self.disabl_on = IntVar()
        check_disabl = ttk.Checkbutton(f3_trends,text = "EDSS Trend", 
                                       variable=self.disabl_on)
        check_disabl.grid(row = 2)
        
    
        ### distribution graphs
        f3_distro = ttk.Frame(f2_options)
        f3_distro.grid(row = 2)
        
        l_distribution = ttk.Label(f3_distro, text = "Distribution Graphs")
        l_distribution.grid(row = 0)
        
        self.distroNeg_on = IntVar()
        check_distroNeg = ttk.Checkbutton(f3_distro, text="Negative", 
                                          variable=self.distroNeg_on)
        check_distroNeg.grid(row = 1)
        
        self.distroNeu_on = IntVar()
        check_distroNeu = ttk.Checkbutton(f3_distro, text="Neutral", 
                                          variable=self.distroNeu_on)
        check_distroNeu.grid(row = 2)
        
        self.distroPos_on = IntVar()
        check_distroPos = ttk.Checkbutton(f3_distro, text="Positive", 
                                          variable=self.distroPos_on)
        check_distroPos.grid(row = 3)
        
        self.distroComp_on = IntVar()
        check_distroComp = ttk.Checkbutton(f3_distro, text="Compound", 
                                          variable=self.distroComp_on)
        check_distroComp.grid(row = 4)
        
        self.scatter_on = IntVar()
        check_scatter = ttk.Checkbutton(f3_distro, text="Scatter", 
                                          variable=self.scatter_on)
        check_scatter.grid(row = 5)
        
        
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
        #store entered user number
        try:
            num = int(self.e_numUsers.get())
            print(f"entered number: {num}")
        except:
            messagebox.showerror("Input Error", "Error: Only Integers Allowed!")
            return
        self.e_numUsers.delete(0, "end")
        
        
        #clear display frame
        for widget in self.displayFrame.winfo_children():
            widget.destroy()

        #build graphs
        
        if (self.sa_on.get() or self.distroNeg_on.get() or 
            self.distroNeu_on.get() or self.distroPos_on.get() or 
            self.distroComp_on.get() or self.scatter_on.get()):
                self.controller.calcSentiments()
        if self.disabl_on.get():
            self.controller.calcEDSS()
            
        self.controller.buildTrendGraphs(num, self.displayFrame, 
                                        self.sa_on, 
                                        self.disabl_on)
        self.controller.buildSentDistribution(self.displayFrame,
                                              self.distroNeg_on,
                                              self.distroNeu_on, 
                                              self.distroPos_on,
                                              self.distroComp_on,
                                              self.scatter_on)
            
        return
    
    def isInt(S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True
        #t3.bell() # .bell() plays that ding sound telling you there was invalid input
        return False