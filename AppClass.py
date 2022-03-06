from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pandas as pd


class App:

    def __init__(self,root):
        root.title("Patient free text explorer")
        root.geometry("900x640")
               
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)       

        self.header_combo_boxes = None

        root_frame = self.configureHomePage(root)
        choose_headers_frame, self.header_combo_boxes = self.configureHeaderSelectFrame(root)    

        # Dictionary to store all of our frames -- frames are essentially a "new page" for our application
        # making it so that we do not need to have multiple windows, rather it can be done all in one window.
        # Widgets (buttons, labels, etc.) can all be added to a frame such that only the top-most frame's widgets
        # are displayed
        
        self.frames_dict = {"root frame":root_frame, "choose headers": choose_headers_frame}
        self.root = root        

        # Display the rootframe
        self.frames_dict["root frame"].tkraise()

        
    def configureHomePage(self,root):
        
        """
        Inputs: (self, root) where root is the parent window of the Tk application

        Configures the homepage frame

        returns: configured homepage frame (type ttk.frame)
        
        """

        root_frame = ttk.Frame(root, padding=(3,3,12,12))
        root_frame.grid(column=0, row=0, sticky=(N,S,E,W))
        root_frame.columnconfigure(1,weight=1)
        root_frame.rowconfigure(1,weight=1)
        root_frame.columnconfigure(0,weight=1)
        root_frame.rowconfigure(0,weight=1)

        title = ttk.Label(root_frame, justify=CENTER, text = "Patient\n\nFree Text\n\nExplorer", font=("bold",25))
        title.grid(column=0, columnspan=2,row=0,rowspan=2)
        load_csv_button = ttk.Button(root_frame, text="Open CSV", command=self.loadCSVClick)
        load_csv_button.grid(column=1, row=3,sticky=(N,S,E,W))
        instruction_button = ttk.Button(root_frame, text="Instructions", command=self.instructionsClick)
        instruction_button.grid(column=0,row=3,sticky=(N,S,E,W))

        return root_frame

    def configureHeaderSelectFrame(self,root):

        """
        Inputs: (self, root) where root is the parent window of the Tk application

        Configures the choose headers frame
        This frame allows the user to select the relevant headers from their CSV file

        returns: configured homepage frame (type ttk.frame), combo boxes (type list of combo boxes)
        
        """
        # Set up the frame, in which all the widgets in this page are placed
        choose_headers = ttk.Frame(root, padding=(3,3,12,12))
        choose_headers.grid(column=0,row=0,sticky=(N,S,E,W))

        ######################## Set up the Labels #######################################################################


        ######################## Set up the ComboBoxes ###################################################################
       

        user_id = ttk.Combobox(choose_headers, textvariable=None)
        user_id.grid(column=0,row=1,sticky=(N,S,E,W))

        dob = ttk.Combobox(choose_headers, textvariable=None)
        dob.grid(column=1,row=1,sticky=(N,S,E,W))

        free_txt = ttk.Combobox(choose_headers, textvariable=None)
        free_txt.grid(column=2,row=1,sticky=(N,S,E,W))

        completed_date = ttk.Combobox(choose_headers, textvariable=None)
        completed_date.grid(column=3,row=1,sticky=(N,S,E,W))

        ms_type = ttk.Combobox(choose_headers, textvariable=None)
        ms_type.grid(column=4,row=1,sticky=(N,S,E,W))

        ms_onset_year = ttk.Combobox(choose_headers, textvariable=None)
        ms_onset_year.grid(column=5,row=1,sticky=(N,S,E,W))

        combo_boxes = [user_id, dob, free_txt, completed_date, ms_type, ms_onset_year]     

        return choose_headers, combo_boxes
        

    def loadCSVClick(self):       
        # Only permit CSV files, returns the full file path
        global csv_file
        csv_file = filedialog.askopenfilename( title="Select a CSV file", filetypes=(("csv files", "*.csv"),))
        self.chooseCSVHeaders()


    def chooseCSVHeaders(self):
        df = pd.read_csv(csv_file)
        # Stores the column headers of the dataframe
        
        self.headers = list(df.columns.values)        
        
        # Add the CSV headers as options for the combo boxes
        for combo_box in self.header_combo_boxes:
            combo_box["values"] = list(self.headers)


        self.frames_dict["choose headers"].tkraise()       


    
    def instructionsClick(self):
        print("Need to display instructions")

       





root = Tk()
App(root)
root.mainloop()