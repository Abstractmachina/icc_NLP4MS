# ChooseCsvHeaders.py
# Class for CSV headers select page 

# where headers are mapped by the user after selecting their CSV file

from tkinter import *
from tkinter import ttk


import pandas as pd

"""
Class for the csv header select page

"""

class ChooseCsvHeaders:

    def __init__(self,root,app,frame,csv_file):
        self.root = root
        self.frame = frame
        self.app = app
        self.csv_file = csv_file
        self.combo_boxes = None
        self.configureHeaderSelectFrame()

    
    def configureHeaderSelectFrame(self):

        """
        Inputs: (self, root) where root is the parent window of the Tk application

        Configures the choose headers frame
        This frame allows the user to select the relevant headers from their CSV file

        returns: configured homepage frame (type ttk.frame), combo boxes (type list of combo boxes)
        
        """
        # Set up the frame, in which all the widgets in this page are placed
        
        self.frame.grid(column=0,row=0,sticky=(N,S,E,W))

        ######################## Set up the Labels #######################################################################
        instructions = " Use the drop down menus below to select the header of the csv column that contains the relevant data.\n If there is no such column, select NONE"
        instruction_l = ttk.Label(self.frame, justify=CENTER, text=instructions, font=("bold",14),)
        instruction_l.grid(column=0,row=0,rowspan=2, columnspan=2,padx=10,pady=10,sticky=(N,S,E,W))
        
        user_id_l = ttk.Label(self.frame, text = "Select the column that contains UserIDs", font=("bold"))
        user_id_l.grid(column=0,row=3,padx=10,pady=10)

        dob_l = ttk.Label(self.frame, text = "Select the column that contains users' date of birth", font=("bold"))
        dob_l.grid(column=1,row=3,padx=10,pady=10)

        free_txt_l = ttk.Label(self.frame, text = "Select the column that contains users' free text", font=("bold"))
        free_txt_l.grid(column=0,row=5,padx=10,pady=10)

        completed_date_l = ttk.Label(self.frame, text = "Select the column that contains the date the users completed the survey", font=("bold"))
        completed_date_l.grid(column=1,row=5,padx=10,pady=10)

        ms_type_l = ttk.Label(self.frame, text = "Select the column that contains users' MS type", font=("bold"))
        ms_type_l.grid(column=0,row=7,padx=10,pady=10)

        ms_onset_l = ttk.Label(self.frame, text = "Select the column that contains users' MS onset year", font=("bold"))
        ms_onset_l.grid(column=1,row=7,padx=10,pady=10)

        ######################## Set up the ComboBoxes ###################################################################
       
        user_id = ttk.Combobox(self.frame, textvariable=None)
        user_id.grid(column=0,row=4)

        dob = ttk.Combobox(self.frame, textvariable=None)
        dob.grid(column=1,row=4)

        free_txt = ttk.Combobox(self.frame, textvariable=None)
        free_txt.grid(column=0,row=6)

        completed_date = ttk.Combobox(self.frame, textvariable=None)
        completed_date.grid(column=1,row=6)

        ms_type = ttk.Combobox(self.frame, textvariable=None)
        ms_type.grid(column=0,row=8)

        ms_onset_year = ttk.Combobox(self.frame, textvariable=None)
        ms_onset_year.grid(column=1,row=8)
        
        
        l_edss = ttk.Label(self.frame, 
                           text = "Select the column that contains the EDSS", 
                           font=("bold"))
        l_edss.grid(column=0, row=9, padx=10, pady=10)
        edss = ttk.Combobox(self.frame, textvariable=None)
        edss.grid(column=0,row=10)
        
        l_diagnosis = ttk.Label(self.frame, 
                           text = "Select the column that contains the users' diagnosis date", 
                           font=("bold"))
        l_diagnosis.grid(column=1, row=9, padx=10, pady=10)
        diagnosisDate = ttk.Combobox(self.frame, textvariable=None)
        diagnosisDate.grid(column=1,row=10)
        
        l_gender = ttk.Label(self.frame, 
                           text = "Select the column that contains the users' gender", 
                           font=("bold"))
        l_gender.grid(column=0, row=11, padx=10, pady=10)
        gender = ttk.Combobox(self.frame, textvariable=None)
        gender.grid(column=0,row=12)

        self.combo_boxes = [user_id, dob, free_txt, completed_date, ms_type, ms_onset_year, edss, diagnosisDate, gender]   

        ######################## Set up the Buttons #######################################################################

        # Insert a blank row before the button to put button at bottom of screen
        self.frame.rowconfigure(13, weight = 1)  
        
        # Back button
        back_b = ttk.Button(self.frame, 
                            text = "Back", 
                            command = lambda: self.app.displayFrame("home frame"))
        back_b.grid(column = 0, row = 14, sticky = (N,S,E,W))  
        
        # Done button
        done_b = ttk.Button(self.frame, 
                            text = "Done", 
                            command = lambda: self.app.displayFrame("main frame"))
        done_b.grid(column = 1, row = 14, sticky = (N,S,E,W))  

 
    
    def chooseCSVHeaders(self):

        """
        Reads in the user CSV file as a pandas dataframe 
        and stores the CSV headers as a data variable

        Set all of the headers as options for the combo boxes for the user
        to choose 

        Finally, displays the choose headers page

        """
        
        df = pd.read_csv(self.csv_file)

        # Store the dataframe as an object datamember
        self.df = df
        # Pass the dataframe to the App class as well
        self.app.df = df

        # Stores the column headers of the dataframe        
        self.headers = list(df.columns.values)       
        self.headers.append("NONE") 

        # Add the CSV headers as options for the combo boxes
        for combo_box in self.combo_boxes:
            combo_box["values"] = list(self.headers)
            combo_box.state(["readonly"])
            # Make the default value "NONE"
            combo_box.current(len(self.headers)-1)
        
        # Store the combo boxes in the App Class
        self.app.csv_header_combo_boxes = self.combo_boxes

        # Display the choose headers frame
        self.app.displayFrame("choose headers")  
        