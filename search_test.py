from search import TextSearcher
import pandas as pd
from tkinter import *
from tkinter import ttk
import pytest


class DummyTextSearcher:

    def __init__(self):
        # Load in test dataframe:
        self.df = pd.read_csv("test_csv_files/search_test.csv")
           
        """
        # Create test combo-boxes:
        user_id = ttk.Combobox(self.root, textvariable=None)

        dob = ttk.Combobox(self.root, textvariable=None)

        free_txt = ttk.Combobox(self.root, textvariable=None)

        completed_date = ttk.Combobox(self.root, textvariable=None)

        ms_type = ttk.Combobox(self.root, textvariable=None)

        ms_onset_year = ttk.Combobox(self.root, textvariable=None)
        """
        user_id = None
        dob = None
        free_txt = None
        completed_date = None
        ms_type = None
        ms_onset_year = None

        self.combo_boxes = [user_id, dob, free_txt, completed_date, ms_type, ms_onset_year]   

        self.searcher = TextSearcher(self.df,self.combo_boxes)

@pytest.fixture
def search_tester():
    return DummyTextSearcher()
    
    
def test_remove_punc(search_tester):
    """ Test the punctuation remover function """

    assert search_tester.searcher.removePunctuation("Don't") == "Dont"
    assert search_tester.searcher.removePunctuation("!!!!") == ""
    assert search_tester.searcher.removePunctuation("") == ""
    assert search_tester.searcher.removePunctuation(" ") == " "
    assert search_tester.searcher.removePunctuation("full. stops. should. be. removed.") == "full stops should be removed"
    assert search_tester.searcher.removePunctuation("!!!!!!!hello!!!!!!") == "hello"
    assert search_tester.searcher.removePunctuation("!!!!!!!h******e!l?l.......o!!!!!!") == "hello"
    assert search_tester.searcher.removePunctuation("!!!!!!!h@@@@@@@@@@$$$$******e!l?l.......o!!!!!!") == "hello"
    assert search_tester.searcher.removePunctuation("Testing a longer sentance. Don't change the CASE, but DO remove the text's punctuation!") == "Testing a longer sentance Dont change the CASE but DO remove the texts punctuation"

def test_clean(search_tester):
    """ Test the clean function"""

    assert search_tester.searcher.clean("Don't") == "dont"
    assert search_tester.searcher.clean("special\n chars\n should\n be\n removed\n") == "special chars should be removed"
    assert search_tester.searcher.clean("special\n\t chars\n should\n be\n removed\n") == "special chars should be removed"
    assert search_tester.searcher.clean("HELLO!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n\n\t\t\t\t") == "hello"
    assert search_tester.searcher.clean("") == ""
    assert search_tester.searcher.clean(" a ") == "a"
    assert search_tester.searcher.clean(" Leading and trailing whitespace is removed    ") == "leading and trailing whitespace is removed"
    assert search_tester.searcher.clean("HeL!lo!") == "hello"
    assert search_tester.searcher.clean("I haven't managed to get a good night sleep in 12 years\n. I don't know what to do, can you help?") == "i havent managed to get a good night sleep in 12 years i dont know what to do can you help"

def test_pre_process(search_tester):
    """ Test the pre_process function, which adds a new column to the data frame
        with the cleaned free text 
    """

    search_tester.searcher.preProcessText("free_txt")
    cleaned_df = search_tester.searcher.df
  

    assert cleaned_df["cleaned_txt"][2] == "i havent managed to get a good night sleep in 12 years i dont know what to do can you help"
    assert cleaned_df["cleaned_txt"][3] == "enter lady capulet lady capulet what noise is here nurse o lamentable day lady capulet what is the matter nurse look look o heavy day lady capulet o me o me my child my only life revive look up or i will die with thee help help call help"
    assert cleaned_df["cleaned_txt"][13] == "once more into the brink"
    assert cleaned_df["cleaned_txt"][11] == "a test box with different cases now test punctuation done"



"""
def test_search(search_tester):
    """  """Test the searching of a phrase in a given window"""
"""
    search_tester.searcher.preProcessText("free_txt")

    assert search_tester.searcher.findPhraseInText("brink", "All",[]) == "once more into the brink \n\n\n"
    search_tester.searcher.reset()    
    assert search_tester.searcher.findPhraseInText("brink", "5",[]) == "once more into the brink \n\n\n"
    search_tester.searcher.reset()    
    assert search_tester.searcher.findPhraseInText("brink", "1",[]) == "the brink \n\n\n"
    search_tester.searcher.reset()    
    assert search_tester.searcher.findPhraseInText("once more into the brink", "1",[]) == " once more into the brink \n\n\n"
    search_tester.searcher.reset()    
    assert search_tester.searcher.findPhraseInText("once more into the brink", "All",[]) == " once more into the brink \n\n\n"
    search_tester.searcher.reset()    
    assert search_tester.searcher.findPhraseInText("once more into the brink", "20",[]) == " once more into the brink \n\n\n"
    search_tester.searcher.reset()    

    assert search_tester.searcher.findPhraseInText("lady capulet", "1",[]) == "enter lady capulet lady\n\n\nlady capulet what\n\n\nday lady capulet what\n\n\nday lady capulet o\n\n\n"
    search_tester.searcher.reset()  

# TODO: add tests for the additional information that can be extracted when searching the text
"""