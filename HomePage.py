from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from ChooseCsvHeaders import ChooseCsvHeaders
from ModelPage import ModelPage

# TODO:
    # Write instructions page
    # Specify starred imports explicitly
    
class HomePage:

    def __init__(self,root,frame,app):

        self.root = root
        self.frame = frame
        self.app = app

        # Instantiated on loadCSV click
        self.header_page = None

        self.model_page = ModelPage(self.root,self.app.addPageFrame("model frame",self.root),self.app)
        self.configurePage()
    
    def configurePage(self):
        """        

        Configures the homepage frame/page layout    
        
        """        
        self.frame.grid(column=0, row=0, sticky=(N,S,E,W))
        self.frame.columnconfigure(1,weight=1)
        self.frame.rowconfigure(1,weight=1)
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure(0,weight=1)

        title = ttk.Label(self.frame, justify=CENTER, text = "Patient\n\nFree Text\n\nExplorer", font=("bold",25))
        title.grid(column=0, columnspan=2,row=0,rowspan=2)
        load_csv_button = ttk.Button(self.frame, text="Open CSV", command = self.loadCSVClick)
        load_csv_button.grid(column=1, row=3,sticky=(N,S,E,W))
        instruction_button = ttk.Button(self.frame, text="Instructions", command=self.instructionsClick)
        instruction_button.grid(column=0,row=3,sticky=(N,S,E,W))
        model_button = ttk.Button(self.frame, text="Predict MS Type", command= lambda: self.app.displayFrame("model frame"))
        model_button.grid(column=1,row=4,sticky=(N,S,E,W))

        # Disabled by default
        # Set to normal by ChooseCsvHeaders.chooseCsvHeaders() function
        self.main_menu_button = ttk.Button(self.frame, 
                                           text = "Main Menu", 
                                           state = DISABLED, 
                                           command = lambda: self.app.displayFrame("main frame"))
        self.main_menu_button.grid(column = 0, row = 4, sticky = NSEW)
    
    def loadCSVClick(self):       
        
        """
        Opens a file dialog window that only allows the user to choose a csv file
        
        After a file is selected, set up the relevant data and open the chooseCSVHeaders page

        """

        # Only permit CSV files, returns the full file path        
        csv_file = filedialog.askopenfilename(title = "Select a CSV file", 
                                              filetypes=(("csv files", "*.csv"),
                                                         ))
        if csv_file == "":
            return
        # initialise class for csv page frame
        self.header_page = ChooseCsvHeaders(self.root, 
                                            self.app, 
                                            self.app.addPageFrame("choose headers", 
                                                                  self.root), 
                                            csv_file)
        # set up data for csv page and display the page
        self.header_page.chooseCSVHeaders()
        #self.app.displayFrame("choose headers") # part of above function?

    def instructionsClick(self):
        
        """
        Opens the instruction page which tells the user how to use our software

        """
        print("Need to display instructions")
    

        