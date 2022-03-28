import pandas as pd
import string
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.util import everygrams
import os

class FrequencyAnalyser:
    def __init__(self,df,txt_hd,id_hd):
        
        
        self.df = df
        self.txt_hd = txt_hd
        self.id_hd = id_hd

        # Sets the nltk data path depending on where this application is saved on the users' machine
        cwd = os.getcwd()
        nltk_data_directory = cwd
        nltk_data_directory += "//nltk_data"
        nltk.data.path.append(nltk_data_directory)
        nltk_data_directory = cwd
        nltk_data_directory += "\\nltk_data"
        nltk.data.path.append(nltk_data_directory)

        # Load NLTK Enlgish stopwords
        self.stop_words = stopwords.words("english")

        # Load Medical Terms
        self.loadMedicalCorpus()

        # Preprocess text
        self.preProcess()

    def loadMedicalCorpus(self):
        """ Loads in the medical corpus downloaded 
        from https://github.com/glutanimate/wordlist-medicalterms-en

        Stores the terms as a list data member """

        med_txt_file = open("medical_terms.txt", "r", encoding="utf8")
        self.medical_terms = []

        for line in med_txt_file:
            # We don't want the last char in line as it is a '\n'
            self.medical_terms.append(line[:-1])    
    
    def removePunctuation(self,text):
        """ Input: string
            Method: removes punctuation from string
            Returns : string
        """
        no_punct_list = [char for char in text if char not in string.punctuation]
        no_punct_string = ''.join(no_punct_list)
        return no_punct_string
    
    def wordTokenize(self,text):
        """ Input: string

            Method: Removes punctuation from string and converts it to lower case
                    and word tokenizes the string (converts it to a list of words)

            Returns: list of strings (words) 
        """
        # Check if passed input is a string
        if isinstance(text,str):
            text = self.removePunctuation(text)
            # Convert string to lower case
            text = text.lower()
            # Return a list of words (using NLTK's word_tokenizer)
            return word_tokenize(text)
        # If not instance, return
        return

    def removeStopWords(self,text,extra_stop_words=[]):
        """ Input: text: list of strings (words)
                   extra_stop_words: list of words

            Method: removes the stopwords stored in self.stopwords from the list
                    and words in extra_stop_words

            Returns: list of strings with stopwords removed
        """
        new_text = []
        for word in text:
            # Convert word to lower case for consistency
            lower_case = word.lower()
            if lower_case not in self.stop_words and lower_case not in extra_stop_words:
                new_text.append(lower_case)
        return new_text

    def preProcess(self):
        """ Input: remove_stopwords (boolean)

            Method: Adds a new column to the dataframe with the free text
                    processed (lower case, punctuation removed, word tokenized)
                    and stopwords removed if remove_stopwords is true
            
            Returns: Nothing (modifies stored dataframe)
        """

        # Creates a list, where each element in the list corresponds to a list of
        # preprocessed words for that users' free text entry
        tokenized_txt = [self.wordTokenize(text) for text in self.df[self.txt_hd]]

        """ Create text for all terms with duplicates and no stopwords """
        tokenized_txt_no_stop = [None] * len(tokenized_txt)        
        for index,entry in enumerate(tokenized_txt):
            new_entry = self.removeStopWords(entry)
            tokenized_txt_no_stop[index] = new_entry
            
        # We also want stopwords removed from the medical lexicon
        self.medical_terms_no_stop = self.removeStopWords(self.medical_terms)

        # Convert medical terms to sets for faster lookup
        self.medical_terms = set(self.medical_terms)
        self.medical_terms_no_stop = set(self.medical_terms_no_stop)

        """ Create text for medical terms with duplicates and stopwords """
        tokenized_txt_med = [None] * len(tokenized_txt) 
        for index,entry in enumerate(tokenized_txt):
            new_entry = []
            for word in entry:
                if word in self.medical_terms:
                    new_entry.append(word)
            tokenized_txt_med[index] = new_entry
        
        """ Create text for medical terms with duplicates and no stopwords """
        tokenized_txt_no_stop_med = [None] * len(tokenized_txt) 
        for index,entry in enumerate(tokenized_txt):
            new_entry = []
            for word in entry:
                if word in self.medical_terms_no_stop:
                    new_entry.append(word)
            tokenized_txt_no_stop_med[index] = new_entry
        
        
        # Create a new column in the stored data frame with the processed text
        self.df["all_txt"] = tokenized_txt  
        self.df["no_stop_txt"] = tokenized_txt_no_stop
        self.df["all_txt_med"] = tokenized_txt_med 
        self.df["no_stop_txt_med"] = tokenized_txt_no_stop_med
        
        """ Get unique all words for each user"""
        self.seen_user_words = {}
        for index,row in self.df.iterrows():
            if row["all_txt"] != None:
                for word in row["all_txt"]:
                    if row[self.id_hd] in self.seen_user_words:
                        if word in self.seen_user_words[row[self.id_hd]]:
                            continue
                        current_words = self.seen_user_words[row[self.id_hd]] 
                        current_words += [word]
                        self.seen_user_words[row[self.id_hd]] = current_words
                    else:
                        self.seen_user_words[row[self.id_hd]] = [word]

        self.seen_user_words = list(self.seen_user_words.values())
        
        # Want just a list of words, currently we have a list of lists
        self.seen_user_words = [word for entries in self.seen_user_words for word in entries]

        """ Get unique words without stopwords for each user"""
        self.seen_user_words_no_stop = {}
        for index,row in self.df.iterrows():
            if row["no_stop_txt"] != None:
                for word in row["no_stop_txt"]:
                    if row[self.id_hd] in self.seen_user_words_no_stop:
                        if word in self.seen_user_words_no_stop[row[self.id_hd]]:
                            continue
                        current_words = self.seen_user_words_no_stop[row[self.id_hd]] 
                        current_words += [word]
                        self.seen_user_words_no_stop[row[self.id_hd]] = current_words
                    else:
                        self.seen_user_words_no_stop[row[self.id_hd]] = [word]
        
        self.seen_user_words_no_stop = list(self.seen_user_words_no_stop.values())

        # Want just a list of words, currently we have a list of lists
        self.seen_user_words_no_stop = [word for entries in self.seen_user_words_no_stop for word in entries]
       
        
        # Special padding characters to prevent n-grams overlapping from users
        # We assume a maximimum of n=4 quad?grams
        for entry in tokenized_txt:
            entry +=["</s>","</s>","</s>","</s>"]

        




    def getFrequencyOfNgram(self,phrase,ngram=1,stopwords=True,medical=False,duplicates=False):
        """
            Inputs: Phrase (string) - the phrase to return the frequency of
                   ngram (int, max=4) - number of words in the phrase
                   stopwords (bool) - True (default) if stopwords should be removed
                   medical (bool) - True if only words in the medical lexicon should be considered (default False)
                   duplicates (bool)  - True if multiple of the same words per user should count towards frequency (default False)

            Method: Calculates the frequency of a given phrase in the free text

            Returns: Frequency of phrase (int)

        """

        if stopwords:
            txt_head = "no_stop_txt"
        else:
            txt_head = "all_txt"
        if medical:
            txt_head += "_med"


        if duplicates == True:
            
            # Combine all text entries
            all_text = []
            for index,row in self.df.iterrows():
                if row[txt_head] != None:
                    for word in row[txt_head]:
                        all_text.append(word)
            # Create frequency distribution
            n_grams = list(everygrams(all_text,ngram,ngram))
            n_grams = [' '.join(word) for word in n_grams]
            freq_dist = FreqDist(n_grams)
            return freq_dist[phrase]     

        if medical == False and duplicates == False:
            if stopwords:
                n_grams = list(everygrams(self.seen_user_words_no_stop,ngram,ngram))  
            else:
                n_grams = list(everygrams(self.seen_user_words,ngram,ngram))  
            n_grams = [' '.join(word) for word in n_grams]
            freq_dist = FreqDist(n_grams)
            return freq_dist[phrase]   

    
    def getMostFrequentNgrams(self,phrase,ngram=1,size=10,stopwords=True,medical=False,duplicates=False):
        """"""
    
    def graphMostFrequentNgrams(self):
        """"""

