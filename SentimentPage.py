import os

from tkinter import *
from tkinter import ttk, filedialog, messagebox

from SentimentController import SentimentController



class SentimentPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app
        self.searchBox = None   #search box that contains user input
        self.displayFrame = None #frame where generated profile is displayed
        self.controller = SentimentController()
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
        #OBSOLETE
        # f2_loadCSV = ttk.Frame(f_controls)
        # f2_loadCSV.grid(row = 0)
        
        # l_loadFile = ttk.Label(f2_loadCSV, text="Load CSV File")
        # l_loadFile.grid(row = 0)
        # b_loadFile = ttk.Button(f2_loadCSV, text = "Open File", 
        #                         command = lambda: self.loadFile_click())
        # b_loadFile.grid(row = 1)
        
        
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
        self.check_sa = ttk.Checkbutton(f2_options, text = "Sentiment Analysis", 
                                   variable=self.sa_on)
        self.check_sa.grid(row = 1)

        
        self.disabl_on = IntVar()
        self.check_disabl = ttk.Checkbutton(f2_options,text = "Disability Score (EDSS)", 
                                       variable=self.disabl_on)
        self.check_disabl.grid(row = 2)
        
        self.combine_on = IntVar()
        self.check_combine = ttk.Checkbutton(f2_options, text = "Combine", 
                                        variable=self.combine_on)
        self.check_combine.grid(row = 4)
        
        
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
        f_display.grid(column = 1, row = 1, sticky=(N,S,E, W))

            
        canvas = Canvas(f_display)
        canvas.grid(row = 0, column = 0, sticky=(N,S,E, W))
        
        scrollbar = ttk.Scrollbar(f_display, orient=VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column = 1, sticky=(N,S))
        
        canvas.configure(yscrollcommand=scrollbar.set)

        self.f2_container = ttk.Frame(canvas)
        self.f2_container.grid(sticky=(N,S,E, W))
        self.f2_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.f2_container, anchor="nw")
        
        for i in range(50):
             Button(self.f2_container, text=f'Button {1+i} Yoo!', font="arial 20").grid(sticky=(W,E))

        results = Text(self.f2_container, width=95, height=20)
        results.grid(row=0, column = 0, sticky=(E,W))
        results.insert("1.0","Result will appear here")
        results.configure(font="16")
        results.configure(state="disabled")
        
        
        return
    
    def validateAndInit(self):       
        h = self.app.csv_header_combo_boxes
        #userId
        if h[0].get() == "NONE":
            messagebox.showerror("Input Error", "Error: User ID required")
            return
        #value
        if h[2].get() == "NONE":
            self.check_sa.configure(state="disabled")
            self.check_combine.configure(state="disabled")
        #edss
        if h[6].get() == "NONE":
            self.check_disabl.configure(state="disabled")
            self.check_combine.configure(state="disabled")
        #date
        if h[3].get() == "NONE":
            messagebox.showerror("Input Error", "Error: Completed Date required")
            return
        
        #import and standardize headers
        self.controller.validateCSV(self.app.df, self.app.csv_header_combo_boxes)
        
        #display this page
        self.app.displayFrame("sent frame")
        return
        
        
    def loadFile_click(self):
        """
        OBSOLETE
        
        """
        file = filedialog.askopenfile(mode="r", 
                                      filetypes=[("CSV Files", "*.csv")])
        if file:
            filepath = os.path.abspath(file.name)
            self.controller.loadCSV(filepath)
        return
        
    def generate_click(self) :
        #store entered user id
        #TODO: sanity check, only ints allowed
        try:
            userId = int(self.searchBox.get())
        except:
            messagebox.showerror("Input Error", "Error: Only Integers Allowed!")
            return
        self.searchBox.delete(0, "end")
        
        #clear display frame
        for widget in self.f2_container.winfo_children():
            widget.destroy()

        #build graphs
        self.controller.buildUserGraphs(userId, self.f2_container, 
                                        self.sa_on, self.disabl_on,
                                        self.combine_on)
            
        #create user info header
        userInfo = self.controller.buildUserInfo(userId)
        r = Text(self.f2_container, width = 95, height = 10)
        r.insert("end", userInfo)
        
        #list free text
        if self.freetxt_on.get():
            ft = self.controller.getFreeTxt(userId)
            r.insert("end", ft)
            
        r.configure(font="10")
        r.configure(state= "disabled")
        r.grid(row=0, column = 0, sticky=(N,S,E,W))
        
            
        # r_scroll = ttk.Scrollbar(self.displayFrame, orient=VERTICAL, command=r.yview)
        # r_scroll.grid(row=0, column=1, rowspan = 1, sticky=(N,S))
        # r["yscrollcommand"] = r_scroll.set
        return