import pandas as pd
import string
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
import os

class FrequencyAnalyser:
    def __init__(self,df):
        
        
        self.df = df

        # Sets the nltk data path depending on where this application is saved on the users' machine
        cwd = os.getcwd()
        nltk_data_directory = cwd
        nltk_data_directory += "//nltk_data"
        nltk.data.path.append(nltk_data_directory)
        nltk_data_directory = cwd
        nltk_data_directory += "\\nltk_data"
        nltk.data.path.append(nltk_data_directory)

    def loadMedicalCorpus(self):
        """"""

    def preProcess(self):
        """"""
    
    def getFrequencyOfNgram(self,phrase,ngram=1,stopwords=True,medical=False):
        """"""
    
    def getMostFrequentNgrams(self,phrase,ngram=1,size=10,stopwords=True,medical=False):
        """"""
    
    def graphMostFrequentNgrams(self):
        """"""

