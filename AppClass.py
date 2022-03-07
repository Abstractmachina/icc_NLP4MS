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
        instructions = " Use the drop down menus below to select the header of the csv column that contains the relevant data.\n If there is no such column, select NONE"
        instruction_l = ttk.Label(choose_headers, justify=CENTER, text=instructions, font=("bold",14),)
        instruction_l.grid(column=0,row=0,rowspan=2, columnspan=2,padx=10,pady=10,sticky=(N,S,E,W))
        
        user_id_l = ttk.Label(choose_headers, text = "Select the column that contains UserIDs", font=("bold"))
        user_id_l.grid(column=0,row=3,padx=10,pady=10)

        dob_l = ttk.Label(choose_headers, text = "Select the column that contains users' date of birth", font=("bold"))
        dob_l.grid(column=1,row=3,padx=10,pady=10)

        free_txt_l = ttk.Label(choose_headers, text = "Select the column that contains users' free text", font=("bold"))
        free_txt_l.grid(column=0,row=5,padx=10,pady=10)

        completed_date_l = ttk.Label(choose_headers, text = "Select the column that contains the date the users completed the survey", font=("bold"))
        completed_date_l.grid(column=1,row=5,padx=10,pady=10)

        ms_type_l = ttk.Label(choose_headers, text = "Select the column that contains users' MS type", font=("bold"))
        ms_type_l.grid(column=0,row=7,padx=10,pady=10)

        ms_onset_l = ttk.Label(choose_headers, text = "Select the column that contains users' MS onset year", font=("bold"))
        ms_onset_l.grid(column=1,row=7,padx=10,pady=10)

        ######################## Set up the ComboBoxes ###################################################################
       
        user_id = ttk.Combobox(choose_headers, textvariable=None)
        user_id.grid(column=0,row=4)

        dob = ttk.Combobox(choose_headers, textvariable=None)
        dob.grid(column=1,row=4)

        free_txt = ttk.Combobox(choose_headers, textvariable=None)
        free_txt.grid(column=0,row=6)

        completed_date = ttk.Combobox(choose_headers, textvariable=None)
        completed_date.grid(column=1,row=6)

        ms_type = ttk.Combobox(choose_headers, textvariable=None)
        ms_type.grid(column=0,row=8)

        ms_onset_year = ttk.Combobox(choose_headers, textvariable=None)
        ms_onset_year.grid(column=1,row=8)

        combo_boxes = [user_id, dob, free_txt, completed_date, ms_type, ms_onset_year]   

        ######################## Set up the Buttons #######################################################################

        done_b = ttk.Button(choose_headers, text="Done", command= lambda: self.frames_dict["root frame"].tkraise())
        done_b.grid(column=0,row=10,columnspan=2,sticky=(N,S,E,W))  

        # Insert a blank row before the button to put button at bottom of screen
        choose_headers.rowconfigure(9,weight=1)
       

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
        self.headers.append("NONE") 
        
        # Add the CSV headers as options for the combo boxes
        for combo_box in self.header_combo_boxes:
            combo_box["values"] = list(self.headers)
            combo_box.state(["readonly"])
            # Make the default value "NONE"
            combo_box.current(len(self.headers)-1)

        # Display the choose headers frame
        self.frames_dict["choose headers"].tkraise()       


    
    def instructionsClick(self):
        print("Need to display instructions")

       





root = Tk()
App(root)
root.mainloop()