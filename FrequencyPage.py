# FrequencyPage.py
# configures the UI for the Word Frequency Analysis page/frame

# Dicts are created on page load - searches can then be performed instantly

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import pandas as pd

from FrequencyAnalyser import FrequencyAnalyser

class FrequencyPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app
        self.analyser = None

        self.configureFreqPage()
    
    # configuration (called on initialisation)
    def configureFreqPage(self):

        # RESULTS BOX #
        
        # Configure the area where frequency results will be displayed
        results = Text(self.frame, width=95, height=20)
        results.grid(row=0,column=0,rowspan=3,columnspan=3,sticky=(N,S,E,W))
        results.insert("1.0","Frequency results will appear here")
        results.configure(font="16")
        results.configure(state="disabled")

        self.display_results = results    
        
        # Configure the results scrollbar - *for 'list most freq' only?*
        results_scroll = ttk.Scrollbar(self.frame, orient=VERTICAL, command=results.yview)
        results_scroll.grid(row=0,column=3,rowspan=3,sticky=(N,S))
        results["yscrollcommand"] = results_scroll.set
        
        # SEARCH #
        
        search_header = ttk.Label(self.frame, anchor = CENTER, text = "Find phrase frequency in data")
        search_header.grid(column = 0, row = 3, columnspan = 2, pady = 8, sticky = NSEW)

        # Search box
        freq_phrase = StringVar()
        freq_box = ttk.Entry(self.frame, textvariable = freq_phrase)
        freq_box.grid(column = 0, row = 4, sticky = (N,S,E,W))

        self.freq_phrase = freq_phrase
        self.freq_box = freq_box

        # 'Get phrase frequency' button
        freq_search_button = ttk.Button(self.frame, 
                                        text = "Get phrase frequency", 
                                        command = lambda: self.freqSearchButtonClick())
        freq_search_button.grid(column=1,row=4,sticky=(N,S,E,W))


        # MOST FREQUENT N-GRAMS #
        
        most_freq_header = ttk.Label(self.frame, anchor = CENTER, text = "Most frequent n-grams in data")
        most_freq_header.grid(column = 0, row = 5, columnspan = 2, pady = 8, sticky = NSEW)
        
        # n-gram list ('n' in 'n-gram)
        ngram_list_label = ttk.Label(self.frame, anchor = CENTER, text = "Number of words in the n-gram")
        ngram_list_label.grid(column = 0, row = 6, sticky = NSEW)
        
        ngram_list = ttk.Combobox(self.frame, textvariable=None)
        ngrams = [1,2,3,4]
        ngram_list["values"] = ngrams
        ngram_list.current(0)
        ngram_list.state(["readonly"])
        ngram_list.grid(column=1, row=6, sticky=(N,S,E,W))
        
        self.ngram_list = ngram_list
        
        # most frequent number list (length of list displayed)
        
        most_frequent_list_label = ttk.Label(self.frame, anchor = CENTER, text = "Length of list")
        most_frequent_list_label.grid(column = 0, row = 7, sticky = NSEW)
        
        most_frequent_list = ttk.Combobox(self.frame, textvariable=None)
        sizes = [5,10,15,20,25,30]
        most_frequent_list["values"] = sizes
        most_frequent_list.current(3)
        most_frequent_list.state(["readonly"])
        most_frequent_list.grid(column = 1, row = 7, sticky = (N,S,E,W))

        self.most_frequent_list = most_frequent_list

        # list freq button
        list_freq_button = ttk.Button(self.frame, 
                                      text = "List most frequent n-grams", 
                                      command = lambda: self.listMostFrequentNgramsClick())
        list_freq_button.grid(column = 0, row = 8, sticky = (N,S,E,W))

        # graph/plot freq button
        graph_freq_button = ttk.Button(self.frame, 
                                       text = "Plot most frequent n-grams", 
                                       command = lambda: self.graphMostFreqNgramsClick())
        graph_freq_button.grid(column = 1, row = 8, sticky = (N,S,E,W))

        self.plot_by_type = IntVar()
        plot_by_type = ttk.Checkbutton(self.frame, 
                                           text = "Plot by MS type", 
                                           variable = self.plot_by_type)
        plot_by_type.grid(column=2,row=8, sticky = W)
        
        # SETTINGS #
        
        settings_header = ttk.Label(self.frame, anchor = CENTER, text = "Settings")
        settings_header.grid(column = 0, row = 9, columnspan = 2, pady = 8, sticky = NSEW)

        # Configure the ms type list
        ms_type_list_label = ttk.Label(self.frame, anchor = CENTER, text = "MS Type")
        ms_type_list_label.grid(column = 0, row = 10, sticky = NSEW)
        
        ms_type_list = ttk.Combobox(self.frame, textvariable=None)
        types = ["All","Benign","PPMS","SPMS","RRMS"]
        ms_type_list["values"] = types
        ms_type_list.current(0)
        ms_type_list.state(["readonly"])
        ms_type_list.grid(column = 1, row = 10, sticky = (N,S,E,W))

        self.ms_type_list = ms_type_list

        # SETTINGS - CHECKBOXES #
        # stopwords
        self.remove_stopwords = IntVar()
        remove_stopwords = ttk.Checkbutton(self.frame, 
                                           text = "Remove Stopwords", 
                                           variable = self.remove_stopwords)
        remove_stopwords.grid(column=0,row=11, sticky = W)

        # only medical words
        self.medical_only = IntVar()
        medical_only = ttk.Checkbutton(self.frame, 
                                       text = "Search Medical Terms Only", 
                                       variable = self.medical_only)
        medical_only.grid(column = 0, row = 12, sticky = W)

        # unique users
        self.unique_only = IntVar()
        unique_only = ttk.Checkbutton(self.frame, 
                                      text = "Only Count A Word Once For All User Entries", 
                                      variable = self.unique_only)
        unique_only.grid(column = 0, row = 13, sticky = W)

        # count word once per text entry
        self.different_entries_only = IntVar()
        different_entries_only = ttk.Checkbutton(self.frame, 
                                                 text = "Only Count A Word Once Per User Entry", 
                                                 variable = self.different_entries_only)
        different_entries_only.grid(column = 0, row = 14, sticky = W)
        
        # BACK BUTTON #

        back_b = ttk.Button(self.frame, 
                            text = "Back", 
                            command = lambda: self.app.displayFrame("main frame"))
        back_b.grid(column = 0, row = 50, pady = 20, sticky=(N,S,E,W))


    # Loads the Word Frequency Analysis page frame (from Main Menu)
    # Heavy function - creates dictionaries from csv
    def validateAndInit(self):
        # validate
        # user ID
        if self.app.csv_header_combo_boxes[0].get() == "NONE":
            messagebox.showerror("Input Error", "Error: User ID required")
            return
        # free text
        if self.app.csv_header_combo_boxes[2].get() == "NONE":
            messagebox.showerror("Input Error", "Error: Free Text required")
            return
        # MS Type
        if self.app.csv_header_combo_boxes[4].get() == "NONE":
            messagebox.showerror("Input Error", "Error: MS Type required")
            return
        # init

        if self.analyser == None:
            self.analyser = FrequencyAnalyser(self.app.df, 
                                            self.app.csv_header_combo_boxes[2].get(), 
                                            self.app.csv_header_combo_boxes[0].get(), 
                                            self.app.csv_header_combo_boxes[4].get())
        self.app.displayFrame("freq frame")

    # 'Get phrase frequency' button (search button) : behaviour
    def freqSearchButtonClick(self):

        freq_search_phrase = self.freq_box.get().strip()
        # change to read in number entered
        # prevent from moving forward with more than 4 words in a phrase
        #ngrams = int(self.ngram_list.get())
        ngrams = count_words_in_string(self.freq_phrase.get())
        if ngrams <= 0 or ngrams > 4:
            self.display_results.configure(state = "normal")
            self.display_results.delete('1.0', 'end')
            self.display_results.insert('1.0', "Please enter a phrase containing 4 words or fewer")
            self.display_results.configure(state = "disabled")
            return
        ms_type = str(self.ms_type_list.get())      

        # Build Boolean variables
        remove_stopwords = False
        medical_only = False
        allow_duplicates = True
        allow_duplicates_across_entries = False
        

        if self.remove_stopwords.get():
            remove_stopwords = True
        if self.medical_only.get():
            medical_only = True
        if self.unique_only.get():
            allow_duplicates = False
        if self.different_entries_only.get():
            allow_duplicates_across_entries = True

        if allow_duplicates == False:
            allow_duplicates_across_entries = False

        frequency_count = self.analyser.getFrequencyOfNgram(freq_search_phrase, 
                                                            ngrams, 
                                                            remove_stopwords, 
                                                            medical_only, 
                                                            allow_duplicates, 
                                                            allow_duplicates_across_entries, 
                                                            ms_type)

        result = "Frequency of the phrase: '"
        result += freq_search_phrase
        result += "' is: "
        result += str(frequency_count)

        self.display_results.configure(state="normal")
        self.display_results.delete('1.0','end')
        self.display_results.insert('1.0',result)
        self.display_results.configure(state="disabled")

    # Button of same name
    def listMostFrequentNgramsClick(self):

        ngrams = int(self.ngram_list.get())
        size = int(self.most_frequent_list.get())
        ms_type = str(self.ms_type_list.get()) 

        # Build Boolean variables
        remove_stopwords = False
        medical_only = False
        allow_duplicates = True
        allow_duplicates_across_entries = False

        if self.remove_stopwords.get():
            remove_stopwords = True
        if self.medical_only.get():
            medical_only = True
        if self.unique_only.get():
            allow_duplicates = False
        if self.different_entries_only.get():
            allow_duplicates_across_entries = True

        if allow_duplicates == False:
            allow_duplicates_across_entries = False

        frequency_list = self.analyser.getMostFrequentNgrams(ngrams, 
                                                             size, 
                                                             remove_stopwords, 
                                                             medical_only, 
                                                             allow_duplicates, 
                                                             allow_duplicates_across_entries, 
                                                             ms_type)
        if frequency_list == '':
            result = "No n-grams found with the given settings."
        else:
            result = "Most frequent "
            result += str(size)
            result += " "
            result += str(ngrams)
            result += " ngrams are: \n"
            result += frequency_list
        
        self.display_results.configure(state="normal")
        self.display_results.delete('1.0','end')
        self.display_results.insert('1.0',result)
        self.display_results.configure(state="disabled")

    # Button of 'same' name ('plot _')
    def graphMostFreqNgramsClick(self):

        ngrams = int(self.ngram_list.get())
        size = int(self.most_frequent_list.get())
        ms_type = str(self.ms_type_list.get()) 

        # Build Boolean variables
        remove_stopwords = False
        medical_only = False
        allow_duplicates = True
        allow_duplicates_across_entries = False

        if self.remove_stopwords.get():
            remove_stopwords = True
        if self.medical_only.get():
            medical_only = True
        if self.unique_only.get():
            allow_duplicates = False
        if self.different_entries_only.get():
            allow_duplicates_across_entries = True

        if allow_duplicates == False:
            allow_duplicates_across_entries = False

        plt_by_type = False

        if self.plot_by_type.get():
            plt_by_type = True

        self.analyser.graphMostFrequentNgrams(ngrams,size,remove_stopwords,medical_only,allow_duplicates,
                                              allow_duplicates_across_entries,ms_type,plot_by_type=plt_by_type)
        
        #
        #
        
# HELPER FUNCTIONS #

def count_words_in_string(string):
    return len(string.split())


#
#
#