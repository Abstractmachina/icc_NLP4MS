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
    
    def generateNgrams(self,n,source_txt):
        """ Input:  n (int) the order of the n-gram
                    source_txt (list of list of tokenized text) where each entry in the 
                    list of lists corresponds to a users' free text response

            Method: generates ngrams from a given source text

            Returns: n_grams_all (list of list of words) where each entry in the list
                     corresponds to a list of n-grams for that users' free text response

        """
        ngrams_all = []
        for index,entry in enumerate(source_txt):
            ngrams = list(everygrams(entry,n,n))
            ngrams = [' '.join(word) for word in ngrams]
            ngrams_all.append(ngrams)
        
        return ngrams_all

    def addUnique(self,dictionary,contents,id):
        """ Input:  dictionary (dict) where unique user entries are stored
                    contents (list) the text to search for unseen words in for the given
                    id (int) the dictionary key for the user
            
            Method: adds any unseen words in contents to id's entry in the dictionary

            Returns: dictionary (dict) with added contents 
        """

        for entry in contents:
            if id in dictionary:
                if entry not in dictionary[id]:
                    current_entry = dictionary[id] 
                    current_entry += [entry]
                    dictionary[id] = current_entry
            else:
                dictionary[id] = [entry]
        return dictionary


    def flattenList(self,list):
        """ Input: list (list) of lists

            Returns: list of lists flattened into just one list
        """
        return [word for entries in list for word in entries]

    def addTokenizedText(self):
        """
            Method: word tokenizes, removes punctuation and converts to lower case the contents
                    of the free text in the data frame. Also does the same for the medical lexcion
                    stored as a datamember.

            Returns: None, stores the tokenized_txt and the tokenized_txt with stopwords removed
                     as class data members, for all of the text, and the text that just contains 
                     medical temrs
        """
        # Creates a list, where each element in the list corresponds to a list of
        # preprocessed words for that users' free text entry
        self.tokenized_txt = [self.wordTokenize(text) for text in self.df[self.txt_hd]]

        # Generate the same, but with stopwords removed
        self.tokenized_txt_no_stop = [None] * len(self.tokenized_txt)        
        for index,entry in enumerate(self.tokenized_txt):
            new_entry = self.removeStopWords(entry)
            self.tokenized_txt_no_stop[index] = new_entry
        
        # We also want stopwords removed from the medical lexicon
        self.medical_terms_no_stop = self.removeStopWords(self.medical_terms)

        # Convert medical terms to sets for faster lookup
        self.medical_terms = set(self.medical_terms)
        self.medical_terms_no_stop = set(self.medical_terms_no_stop)

        """ Create text for medical terms with duplicates and stopwords """
        self.tokenized_txt_med = [None] * len(self.tokenized_txt) 
        for index,entry in enumerate(self.tokenized_txt):
            new_entry = []
            for word in entry:
                if word in self.medical_terms:
                    new_entry.append(word)
            self.tokenized_txt_med[index] = new_entry
        
        """ Create text for medical terms with duplicates and no stopwords """
        self.tokenized_txt_no_stop_med = [None] * len(self.tokenized_txt) 
        for index,entry in enumerate(self.tokenized_txt):
            new_entry = []
            for word in entry:
                if word in self.medical_terms_no_stop:
                    new_entry.append(word)
            self.tokenized_txt_no_stop_med[index] = new_entry
    
    def createNgramsForDf(self):
        """
            Adds new columns to the data frame for each n-gram and lexicon
            combination (medical terms and stopwords)
        """

        self.df["all_txt"] = self.tokenized_txt  
        self.df["no_stop_txt"] = self.tokenized_txt_no_stop
        self.df["all_txt_med"] = self.tokenized_txt_med 
        self.df["no_stop_txt_med"] = self.tokenized_txt_no_stop_med
        
        """ Create bigrams, trigrams and quadgrams for all text"""
        self.df["all_txt_bigrams"] = self.generateNgrams(2,self.tokenized_txt)
        self.df["all_txt_trigrams"] = self.generateNgrams(3,self.tokenized_txt)
        self.df["all_txt_quadgrams"] = self.generateNgrams(4,self.tokenized_txt)

        """ Create bigrams, trigrams and quadgrams for text without stopwords"""
        self.df["no_stop_bigrams"] = self.generateNgrams(2,self.tokenized_txt_no_stop)
        self.df["no_stop_trigrams"] = self.generateNgrams(3,self.tokenized_txt_no_stop)
        self.df["no_stop_quadgrams"] = self.generateNgrams(4,self.tokenized_txt_no_stop)

        """ Create bigrams, trigrams and quadgrams for all medical words in text"""
        self.df["all_txt_bigrams_med"] = self.generateNgrams(2,self.tokenized_txt_med)
        self.df["all_txt_trigrams_med"] = self.generateNgrams(3,self.tokenized_txt_med)
        self.df["all_txt_quadgrams_med"] = self.generateNgrams(4,self.tokenized_txt_med)

        """ Create bigrams, trigrams and quadgrams for medical words without stopwords"""
        self.df["no_stop_bigrams_med"] = self.generateNgrams(2,self.tokenized_txt_no_stop_med)
        self.df["no_stop_trigrams_med"] = self.generateNgrams(3,self.tokenized_txt_no_stop_med)
        self.df["no_stop_quadgrams_med"] = self.generateNgrams(4,self.tokenized_txt_no_stop_med)

    def buildUniqueDictionaries(self,row):

        """ Generate unique values (1 per user for all user entries) for each ngram """
        if row["all_txt"] != None:
            self.seen_user_words_all = self.addUnique(self.seen_user_words_all,row["all_txt"],row[self.id_hd])
        if row["all_txt_bigrams"] != None:
           self.seen_user_bigrams_all = self.addUnique(self.seen_user_bigrams_all,row["all_txt_bigrams"],row[self.id_hd])
        if row["all_txt_trigrams"] != None:
            self.seen_user_trigrams_all = self.addUnique(self.seen_user_trigrams_all,row["all_txt_trigrams"],row[self.id_hd])
        if row["all_txt_quadgrams"] != None:
           self.seen_user_quadgrams_all = self.addUnique(self.seen_user_quadgrams_all,row["all_txt_quadgrams"],row[self.id_hd])
        if row["no_stop_txt"] != None:
            self.seen_user_words_no_stop = self.addUnique(self.seen_user_words_no_stop,row["no_stop_txt"],row[self.id_hd])
        if row["no_stop_bigrams"] != None:
           self.seen_user_bigrams_no_stop = self.addUnique(self.seen_user_bigrams_no_stop,row["no_stop_bigrams"],row[self.id_hd]) 
        if row["no_stop_trigrams"] != None:
            self.seen_user_trigrams_no_stop = self.addUnique(self.seen_user_trigrams_no_stop,row["no_stop_trigrams"],row[self.id_hd]) 
        if row["no_stop_quadgrams"] != None:
            self.seen_user_quadgrams_no_stop = self.addUnique(self.seen_user_quadgrams_no_stop,row["no_stop_quadgrams"],row[self.id_hd]) 
        if row["all_txt_med"] != None:
            self.seen_user_words_all_med = self.addUnique(self.seen_user_words_all_med,row["all_txt_med"],row[self.id_hd])
        if row["all_txt_bigrams_med"] != None:
            self.seen_user_bigrams_all_med = self.addUnique(self.seen_user_bigrams_all_med,row["all_txt_bigrams_med"],row[self.id_hd])
        if row["all_txt_trigrams_med"] != None:
            self.seen_user_trigrams_all_med = self.addUnique(self.seen_user_trigrams_all_med,row["all_txt_trigrams_med"],row[self.id_hd])
        if row["all_txt_quadgrams_med"] != None:
            self.seen_user_quadgrams_all_med = self.addUnique(self.seen_user_quadgrams_all_med,row["all_txt_quadgrams_med"],row[self.id_hd])
        if row["no_stop_txt_med"] != None:
            self.seen_user_words_no_stop_med = self.addUnique(self.seen_user_words_no_stop_med,row["no_stop_txt_med"],row[self.id_hd])
        if row["no_stop_bigrams_med"] != None:
            self.seen_user_bigrams_no_stop_med = self.addUnique(self.seen_user_bigrams_no_stop_med,row["no_stop_bigrams_med"],row[self.id_hd])
        if row["no_stop_trigrams_med"] != None:
            self.seen_user_trigrams_no_stop_med = self.addUnique(self.seen_user_trigrams_no_stop_med,row["no_stop_trigrams_med"],row[self.id_hd])
        if row["no_stop_quadgrams_med"] != None:
            self.seen_user_quadgrams_no_stop_med = self.addUnique(self.seen_user_quadgrams_no_stop_med,row["no_stop_quadgrams_med"],row[self.id_hd])  

    def buildNoDuplicatesPerEntry(self,row):

        if row["all_txt"] != None:
            self.no_dup_words_all.append(set(row["all_txt"]))
        if row["all_txt_bigrams"] != None:
           self.no_dup_bigrams_all.append(set(row["all_txt_bigrams"]))
        if row["all_txt_trigrams"] != None:
            self.no_dup_trigrams_all.append(set(row["all_txt_trigrams"]))
        if row["all_txt_quadgrams"] != None:
           self.no_dup_quadgrams_all.append(set(row["all_txt_quadgrams"]))
        if row["no_stop_txt"] != None:
            self.no_dup_words_no_stop.append(set(row["no_stop_txt"]))
        if row["no_stop_bigrams"] != None:
           self.no_dup_bigrams_no_stop.append(set(row["no_stop_bigrams"])) 
        if row["no_stop_trigrams"] != None:
            self.no_dup_trigrams_no_stop.append(set(row["no_stop_trigrams"]))
        if row["no_stop_quadgrams"] != None:
            self.no_dup_quadgrams_no_stop.append(set(row["no_stop_quadgrams"]))
        if row["all_txt_med"] != None:
            self.no_dup_words_all_med.append(set(row["all_txt_med"]))
        if row["all_txt_bigrams_med"] != None:
            self.no_dup_bigrams_all_med.append(set(row["all_txt_bigrams_med"]))
        if row["all_txt_trigrams_med"] != None:
            self.no_dup_trigrams_all_med.append(set(row["all_txt_trigrams_med"]))
        if row["all_txt_quadgrams_med"] != None:
            self.no_dup_quadgrams_all_med.append(set(row["all_txt_quadgrams_med"]))
        if row["no_stop_txt_med"] != None:
            self.no_dup_words_no_stop_med.append(set(row["no_stop_txt_med"]))
        if row["no_stop_bigrams_med"] != None:
            self.no_dup_bigrams_no_stop_med.append(set(row["no_stop_bigrams_med"]))
        if row["no_stop_trigrams_med"] != None:
            self.no_dup_trigrams_no_stop_med.append(set(row["no_stop_trigrams_med"]))
        if row["no_stop_quadgrams_med"] != None:
            self.no_dup_quadgrams_no_stop_med.append(set(row["no_stop_quadgrams_med"]))
    
    def createLexiconsOfUniqueUserWords(self):
        
        self.unique_words_all = self.flattenList(list(self.seen_user_words_all.values()))
        self.unique_bigrams_all = self.flattenList(list(self.seen_user_bigrams_all.values()))
        self.unique_trigrams_all = self.flattenList(list(self.seen_user_trigrams_all.values()))
        self.unique_quadgrams_all = self.flattenList(list(self.seen_user_quadgrams_all.values()))

        self.unique_words_no_stop = self.flattenList(list(self.seen_user_words_no_stop.values()))
        self.unique_bigrams_no_stop = self.flattenList(list(self.seen_user_bigrams_no_stop.values()))
        self.unique_trigrams_no_stop = self.flattenList(list(self.seen_user_trigrams_no_stop.values()))
        self.unique_quadgrams_no_stop = self.flattenList(list(self.seen_user_quadgrams_no_stop.values()))

        self.unique_words_all_med = self.flattenList(list(self.seen_user_words_all_med.values()))
        self.unique_bigrams_all_med = self.flattenList(list(self.seen_user_bigrams_all_med.values()))
        self.unique_trigrams_all_med = self.flattenList(list(self.seen_user_trigrams_all_med.values()))
        self.unique_quadgrams_all_med = self.flattenList(list(self.seen_user_quadgrams_all_med.values()))

        self.unique_words_no_stop_med = self.flattenList(list(self.seen_user_words_no_stop_med.values()))
        self.unique_bigrams_no_stop_med = self.flattenList(list(self.seen_user_bigrams_no_stop_med.values()))
        self.unique_trigrams_no_stop_med = self.flattenList(list(self.seen_user_trigrams_no_stop_med.values()))
        self.unique_quadgrams_no_stop_med = self.flattenList(list(self.seen_user_quadgrams_no_stop_med.values()))
    
    def createLexiconsOfNoDuplicatesPerEntry(self):
        
        self.no_dup_words_all = self.flattenList(self.no_dup_words_all)
        self.no_dup_bigrams_all = self.flattenList(self.no_dup_bigrams_all)
        self.no_dup_trigrams_all = self.flattenList(self.no_dup_trigrams_all)
        self.no_dup_quadgrams_all = self.flattenList(self.no_dup_quadgrams_all)

        self.no_dup_words_no_stop = self.flattenList(self.no_dup_words_no_stop)
        self.no_dup_bigrams_no_stop = self.flattenList(self.no_dup_bigrams_no_stop)
        self.no_dup_trigrams_no_stop = self.flattenList(self.no_dup_trigrams_no_stop)
        self.no_dup_quadgrams_no_stop = self.flattenList(self.no_dup_quadgrams_no_stop)

        self.no_dup_words_all_med = self.flattenList(self.no_dup_words_all_med)
        self.no_dup_bigrams_all_med = self.flattenList(self.no_dup_bigrams_all_med)
        self.no_dup_trigrams_all_med = self.flattenList(self.no_dup_trigrams_all_med)
        self.no_dup_quadgrams_all_med = self.flattenList(self.no_dup_quadgrams_all_med)

        self.no_dup_words_no_stop_med = self.flattenList(self.no_dup_words_no_stop_med)
        self.no_dup_bigrams_no_stop_med = self.flattenList(self.no_dup_bigrams_no_stop_med)
        self.no_dup_trigrams_no_stop_med = self.flattenList(self.no_dup_trigrams_no_stop_med)
        self.no_dup_quadgrams_no_stop_med = self.flattenList(self.no_dup_quadgrams_no_stop_med)
    
    def createLexiconswithDuplicates(self):
        
        self.words_all = self.flattenList(list(self.df["all_txt"]))
        self.bigrams_all = self.flattenList(list(self.df["all_txt_bigrams"]))
        self.trigrams_all = self.flattenList(list(self.df["all_txt_trigrams"]))
        self.quadgrams_all = self.flattenList(list(self.df["all_txt_quadgrams"]))

        self.words_no_stop = self.flattenList(list(self.df["no_stop_txt"]))
        self.bigrams_no_stop = self.flattenList(list(self.df["no_stop_bigrams"]))
        self.trigrams_no_stop = self.flattenList(list(self.df["no_stop_trigrams"]))
        self.quadgrams_no_stop = self.flattenList(list(self.df["no_stop_quadgrams"]))

        self.words_all_med = self.flattenList(list(self.df["all_txt_med"]))
        self.bigrams_all_med = self.flattenList(list(self.df["all_txt_bigrams_med"]))
        self.trigrams_all_med = self.flattenList(list(self.df["all_txt_trigrams_med"]))
        self.quadgrams_all_med = self.flattenList(list(self.df["all_txt_quadgrams_med"]))

        self.words_no_stop_med = self.flattenList(list(self.df["no_stop_txt_med"]))
        self.bigrams_no_stop_med = self.flattenList(list(self.df["no_stop_bigrams_med"]))
        self.trigrams_no_stop_med = self.flattenList(list(self.df["no_stop_trigrams_med"]))
        self.quadgrams_no_stop_med = self.flattenList(list(self.df["no_stop_quadgrams_med"]))

    def preProcess(self):
        """ Input: remove_stopwords (boolean)

            Method: Generates the lexicons for all possible bigrams and other option combinations
            
            Returns: Nothing (modifies stored dataframe)
        """

        self.addTokenizedText()   
        self.createNgramsForDf()                
        
        """ Get unique n-grams for each user"""
        self.seen_user_words_all = {}
        self.seen_user_bigrams_all = {}
        self.seen_user_trigrams_all = {}
        self.seen_user_quadgrams_all= {}

        self.seen_user_words_no_stop = {}
        self.seen_user_bigrams_no_stop = {}
        self.seen_user_trigrams_no_stop = {}
        self.seen_user_quadgrams_no_stop= {}

        self.seen_user_words_all_med = {}
        self.seen_user_bigrams_all_med = {}
        self.seen_user_trigrams_all_med = {}
        self.seen_user_quadgrams_all_med= {}

        self.seen_user_words_no_stop_med = {}
        self.seen_user_bigrams_no_stop_med = {}
        self.seen_user_trigrams_no_stop_med = {}
        self.seen_user_quadgrams_no_stop_med= {}

        """ Get n-grams with no dupluicates over a given free text response
            for all users
        """
        self.no_dup_words_all = []
        self.no_dup_bigrams_all = []
        self.no_dup_trigrams_all = []
        self.no_dup_quadgrams_all= []

        self.no_dup_words_no_stop = []
        self.no_dup_bigrams_no_stop = []
        self.no_dup_trigrams_no_stop = []
        self.no_dup_quadgrams_no_stop= []

        self.no_dup_words_all_med = []
        self.no_dup_bigrams_all_med = []
        self.no_dup_trigrams_all_med = []
        self.no_dup_quadgrams_all_med= []

        self.no_dup_words_no_stop_med = []
        self.no_dup_bigrams_no_stop_med = []
        self.no_dup_trigrams_no_stop_med = []
        self.no_dup_quadgrams_no_stop_med= []

        # Build entries for each user entry in the dataframe
        for index,row in self.df.iterrows():
            self.buildUniqueDictionaries(row)   
            self.buildNoDuplicatesPerEntry(row)                 

        """ Generate the 42 lexicons"""
        self.createLexiconswithDuplicates()
        self.createLexiconsOfUniqueUserWords()
        self.createLexiconsOfNoDuplicatesPerEntry() 

        
         
    def getFrequencyOfNgram(self,phrase,ngram=1,stopwords=True,medical=False,allow_duplicates=False,allow_duplcates_across_entries=False):
        """
            Inputs: Phrase (string) - the phrase to return the frequency of
                   ngram (int, max=4) - number of words in the phrase
                   stopwords (bool) - True (default) if stopwords should be removed
                   medical (bool) - True if only words in the medical lexicon should be considered (default False)
                   duplicates (bool)  - True if multiple of the same words per user should count towards frequency (default False)

            Method: Calculates the frequency of a given phrase in the free text

            Returns: Frequency of phrase (int)

        """


        if stopwords and medical and allow_duplcates_across_entries:
            if ngram == 1:
                n_grams = self.no_dup_words_no_stop_med
            elif ngram == 2:
                n_grams = self.no_dup_bigrams_no_stop_med
            elif ngram == 3:
                n_grams = self.no_dup_trigrams_no_stop_med
            elif ngram == 4:
                n_grams = self.no_dup_quadgrams_no_stop_med
        
        elif stopwords and allow_duplcates_across_entries:
            if ngram == 1:
                n_grams = self.no_dup_words_no_stop
            elif ngram == 2:
                n_grams = self.no_dup_bigrams_no_stop
            elif ngram == 3:
                n_grams = self.no_dup_trigrams_no_stop
            elif ngram == 4:
                n_grams = self.no_dup_quadgrams_no_stop
        
        elif medical and allow_duplcates_across_entries:
            if ngram == 1:
                n_grams = self.no_dup_words_all_med
            elif ngram == 2:
                n_grams = self.no_dup_bigrams_all_med
            elif ngram == 3:
                n_grams = self.no_dup_trigrams_all_med
            elif ngram == 4:
                n_grams = self.no_dup_quadgrams_all_med

        elif allow_duplcates_across_entries:
            if ngram == 1:
                n_grams = self.no_dup_words_all
            elif ngram == 2:
                n_grams = self.no_dup_bigrams_all
            elif ngram == 3:
                n_grams = self.no_dup_trigrams_all
            elif ngram == 4:
                n_grams = self.no_dup_quadgrams_all

        elif stopwords and medical and allow_duplicates:
            if ngram == 1:
                n_grams = self.words_no_stop_med
            elif ngram == 2:
                n_grams = self.bigrams_no_stop_med
            elif ngram == 3:
                n_grams = self.trigrams_no_stop_med
            elif ngram == 4:
                n_grams = self.quadgrams_no_stop_med
        
        elif stopwords and allow_duplicates:
            if ngram == 1:
                n_grams = self.words_no_stop
            elif ngram == 2:
                n_grams = self.bigrams_no_stop
            elif ngram == 3:
                n_grams = self.trigrams_no_stop
            elif ngram == 4:
                n_grams = self.quadgrams_no_stop
        
        elif stopwords and medical:
            if ngram == 1:
                n_grams = self.unique_words_no_stop_med
            elif ngram == 2:
                n_grams = self.unique_bigrams_no_stop_med
            elif ngram == 3:
                n_grams = self.unique_trigrams_no_stop_med
            elif ngram == 4:
                n_grams = self.unique_quadgrams_no_stop_med

        
        elif stopwords:
            if ngram == 1:
                n_grams = self.unique_words_no_stop
            elif ngram == 2:
                n_grams = self.unique_bigrams_no_stop
            elif ngram == 3:
                n_grams = self.unique_trigrams_no_stop
            elif ngram == 4:
                n_grams = self.unique_quadgrams_no_stop

        
        elif medical and allow_duplicates:
            if ngram == 1:
                n_grams = self.words_all_med
            elif ngram == 2:
                n_grams = self.bigrams_all_med
            elif ngram == 3:
                n_grams = self.trigrams_all_med
            elif ngram == 4:
                n_grams = self.quadgrams_all_med
        
        elif medical:
            if ngram == 1:
                n_grams = self.unique_words_all_med
            elif ngram == 2:
                n_grams = self.unique_bigrams_all_med
            elif ngram == 3:
                n_grams = self.unique_trigrams_all_med
            elif ngram == 4:
                n_grams = self.unique_quadgrams_all_med
        
        elif allow_duplicates:
            if ngram == 1:
                n_grams = self.words_all
            elif ngram == 2:
                n_grams = self.bigrams_all
            elif ngram == 3:
                n_grams = self.trigrams_all
            elif ngram == 4:
                n_grams = self.quadgrams_all
        
        else:
            if ngram == 1:
                n_grams = self.unique_words_all
            elif ngram == 2:
                n_grams = self.unique_bigrams_all
            elif ngram == 3:
                n_grams = self.unique_trigrams_all
            elif ngram == 4:
                n_grams = self.unique_quadgrams_all
               
        freq_dist = FreqDist(n_grams)
        return freq_dist[phrase]   


    
    def getMostFrequentNgrams(self,phrase,ngram=1,size=10,stopwords=True,medical=False,duplicates=False):
        """"""
    
    def graphMostFrequentNgrams(self):
        """"""

