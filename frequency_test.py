import pytest
from FrequencyAnalyser import FrequencyAnalyser
import pandas as pd



class FrequencyTester:
    def __init__(self):
        # Load in the test data frame
        self.df = pd.read_csv("freq_test.csv")

        self.FreqAnalyser = FrequencyAnalyser(self.df,"free_txt","user_id")

@pytest.fixture
def freq_tester():
    return FrequencyTester()

def test_frequency_counts_duplicates(freq_tester):
     
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("brink",1,stopwords=True,medical=False,duplicates=True) == 1
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("lady capulet",2,stopwords=True,medical=False,duplicates=True) == 4
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("civil blood makes",3,stopwords=True,medical=False,duplicates=True) == 1
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("enter",1,stopwords=True,medical=False,duplicates=True) == 2
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("a",1,stopwords=False,medical=False,duplicates=True) == 18

def test_frequency_counts_med_duplicates(freq_tester):
     
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("brink",1,stopwords=True,medical=True,duplicates=True) == 0
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("lady",1,stopwords=True,medical=True,duplicates=True) == 0
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("lady capulet",2,stopwords=True,medical=True,duplicates=True) == 0
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("blood",1,stopwords=True,medical=True,duplicates=True) == 5
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("patient",1,stopwords=True,medical=True,duplicates=True) == 1
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("blood pressure",2,stopwords=True,medical=True,duplicates=True) == 4
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("high blood pressure",3,stopwords=True,medical=True,duplicates=True) == 2



def test_frequency_counts_no_duplicates(freq_tester):
    
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("the",1,stopwords=False,medical=False,duplicates=False) == 7
    assert freq_tester.FreqAnalyser.getFrequencyOfNgram("lady capulet",2,stopwords=False,medical=False,duplicates=False) == 1

    